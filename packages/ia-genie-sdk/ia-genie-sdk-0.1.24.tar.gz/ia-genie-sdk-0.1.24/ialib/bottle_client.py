"""Implements the "Bottle" interface."""
import functools
import io
import json
import uuid
from typing import Dict, List, Any, Tuple, Union

import requests

from ialib.genome_info import Genome


class BottleQueryError(BaseException):
    """Raised if any query to any node returns an error."""
    pass


class BottleConnectionError(BaseException):
    """Raised if connecting to any node returns an error."""
    pass


def _ensure_connected(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        if not self._connected:
            raise BottleConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries'
            )
        return f(self, *args, **kwargs)

    return inner


def _remove_unique_id(response: dict) -> dict:
    """Return *response* with the key 'unique_id' removed regardless of nesting."""
    if isinstance(response, dict):
        if 'unique_id' in response:
            del response['unique_id']
        for value in response.values():
            if isinstance(value, dict):
                _remove_unique_id(value)
    return response


class BottleClient:
    """Interface for interacting with bottles."""

    def __init__(self, bottle_info):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

        """
        self.genome = None
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = []
        self.query_nodes = []
        self.headers = {'X-API-KEY': self.api_key}
        self.all_nodes = []
        self._connected = False
        self.genome = None
        self.genie = None
        self.send_unique_ids = True
        self.summarize_for_single_node = True
        if 'secure' not in self.bottle_info or self.bottle_info['secure']:
            self.secure = True
            self.url = 'https://{name}.{domain}/'.format(**self.bottle_info)
        else:
            self.secure = False
            self.url = 'http://{name}.{domain}/'.format(**self.bottle_info)

    def __repr__(self) -> str:
        return (
            '<{name}.{domain}| secure: %r, connected: %s, genie: %s, \
                  ingress_nodes: %i, query_nodes: %i>'.format(
                **self.bottle_info
            )
            % (
                self.secure,
                self._connected,
                self.genie,
                len(self.ingress_nodes),
                len(self.query_nodes),
            )
        )

    def receive_unique_ids(self, should_set: bool = True) -> bool:
        self.send_unique_ids = should_set
        return self.send_unique_ids

    def connect(self) -> Dict:
        """Grabs the bottle's genie's genome for node definitions."""
        response_data = requests.get(self.url + 'connect', verify=self.secure, headers=self.headers).json()
        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise BottleConnectionError("Connection failed!", response_data)

        self.genome = Genome(response_data['genome'])
        self.genie = response_data['genome']['agent']
        self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        if response_data['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': response_data['connection'], 'genie': response_data['genie']}

    def set_ingress_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define where data will be sent."""
        if nodes is None:
            nodes = []
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.ingress_nodes

    def set_query_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define which nodes should return answers."""
        if nodes is None:
            nodes = []
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.query_nodes

    def _query(
        self, query_method: Any, path: str, data: Union[dict, str] = None, nodes: List = None, unique_id: str = None
    ) -> Union[dict, Tuple[dict, str]]:
        """Internal helper function to make a REST API call with the given *query* and *data*."""
        if not self._connected:
            raise BottleConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries'
            )
        result = {}
        if unique_id is not None:
            if data:
                data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}

        if isinstance(nodes[0], str):
            nodes = [{'name': name, 'id': self.genome.primitive_map[name]} for name in nodes]
        for node in nodes:
            full_path = f'{self.url}{node["id"]}/{path}'
            try:
                if data is not None:
                    response = query_method(full_path, verify=self.secure, headers=self.headers, json={'data': data})
                else:
                    response = query_method(full_path, verify=self.secure, headers=self.headers)
                response.raise_for_status()
                response = response.json()
                if response['status'] != 'okay':
                    raise BottleQueryError(response['message'])
                if not self.send_unique_ids:
                    response = _remove_unique_id(response['message'])
                else:
                    response = response['message']
                if len(nodes) == 1 and self.summarize_for_single_node:
                    result = response
                else:
                    result[node['name']] = response
            except Exception as exception:
                raise BottleQueryError(str(exception)) from None
        if unique_id is not None:
            return result, unique_id
        return result

    def set_summarize_for_single_node(self, value: bool):
        """When True, queries against a single node return responses directly instead of in a dict key."""
        self.summarize_for_single_node = value

    def observe(self, data: Dict, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'observe', data=data, nodes=nodes)

    def observe_event(self, data: Dict, unique_id: str = None) -> Tuple[dict, str]:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        results = {}
        uid = None
        if unique_id is None:
            unique_id = str(uuid.uuid4())
        for node, node_data in data.items():
            response, uid = self._query(requests.post, 'observe', data=node_data, nodes=[node], unique_id=unique_id)
            results[node] = response
        return results, uid

    @_ensure_connected
    def observe_classification(self, data=None, nodes: List = None):
        """Send a classification to all nodes as a singular symbol in the last event.

        Sending the classification as a single symbol in the last event is the canonical way to classify a sequence.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query("observe", data, nodes=nodes)

    def show_status(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return the current status of the bottle."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'status', nodes=nodes)

    def learn(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return the learn results."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'learn', nodes=nodes)

    def get_wm(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return information about Working Memory."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'working-memory', nodes=nodes)

    def get_predictions(self, unique_id: str = None, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return prediction result data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'predictions', nodes=nodes, unique_id=unique_id)

    def get_hive_prediction_utility(self) -> dict:
        """Return prediction result data."""
        return requests.post(
            f'{self.url}predictions/utility',
            headers=self.headers,
            json={'data': {'primitive_ids': [primitive['id'] for primitive in self.query_nodes]}},
        ).json()

    def clear_wm(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clear the Working Memory of the Genie."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'working-memory/clear', nodes=nodes)

    def clear_all_memory(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clear both the Working Memory and persisted memory."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'clear-all-memory', nodes=nodes)

    def get_percept_data(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return percept data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'percept-data', nodes=nodes)

    def get_cognition_data(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return cognition data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'cognition-data', nodes=nodes)

    def get_decision_table(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return a decision table."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'decision-table', nodes=nodes)

    def get_action_data(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return action data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'action-data', nodes=nodes)

    @_ensure_connected
    def change_genes(self, gene_data: Dict, nodes: List = None) -> Union[dict, Any]:
        """Change the genes in *gene_data* to their associated values.

        This will do live updates to an existing agent, rather than stopping an agent and starting a new one, as
        per 'injectGenome'.
        gene_data of form:

            {gene: value}

        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]

        result = {}
        for node in nodes:
            response = requests.post(
                f"{self.url}{node['id']}/genes/change",
                verify=self.secure,
                headers=self.headers,
                json={'data': gene_data},
            ).json()
            if 'error' in response or response['status'] == 'failed':
                if len(nodes) == 1 and self.summarize_for_single_node:
                    raise BottleQueryError(response)
            self.genome.change_genes(node['id'], gene_data)
            if len(nodes) == 1 and self.summarize_for_single_node:
                return response['message']
            result[node['name']] = response['message']
        return result

    @_ensure_connected
    def inject_genome(self, genome: Dict) -> Dict:
        """Halt all primitives in the current bottle and start those described in *genome*.

        *genome* must be either a JSON-serializable object or a file-like object.
        """
        if isinstance(genome, io.TextIOBase):
            genome = json.load(genome)
        response = requests.post(
            f'{self.url}genome/inject', verify=self.secure, headers=self.headers, json={'genome': genome}
        ).json()
        if 'error' not in response:
            self.genome = Genome(genome)
            self.genie = self.genome.agent
            self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        return response

    @_ensure_connected
    def get_cost_benefit(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return cost benefit."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'getCostBenefit', nodes=nodes)

    @_ensure_connected
    def get_gene(self, gene: str, nodes: List = None) -> Union[dict, Dict[Any, Dict[str, Any]]]:
        """Return the value for the gene *gene* on *nodes*."""
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.get(
                    f"{self.url}{node['id']}/gene/{gene}", verify=self.secure, headers=self.headers
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise BottleQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {gene: response['message']}
                result[node['name']] = {gene: response['message']}
            except BaseException as exception:
                raise BottleQueryError(exception) from None

        return result

    @_ensure_connected
    def get_model(self, model_name: str, nodes: List = None) -> Union[dict, Any]:
        """Returns model with name *model_name*.

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found.
        """
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.get(
                    f"{self.url}{node['id']}/model/{model_name}", headers=self.headers, verify=self.secure
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise BottleQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise BottleQueryError(str(exception)) from None

        return result

    def get_name(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return name of *nodes*."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'name', nodes=nodes)

    def get_time(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Return time on *nodes*."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'time', nodes=nodes)

    @_ensure_connected
    def get_vector(self, vector_name: str, nodes: List = None) -> Union[dict, Dict[Any, Dict[str, Any]]]:
        """Return the vector with *vector_name* on *nodes* (it will be present on at most one)."""
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.get(
                    f"{self.url}{node['id']}/vector", headers=self.headers, verify=self.secure, json={'data': vector_name}
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise BottleQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                raise BottleQueryError(str(exception)) from None

        return result

    @_ensure_connected
    def increment_recall_threshold(self, increment: float, nodes: List = None) -> Dict[Any, Dict[str, Any]]:
        """Increment recall threshold by *increment* on *nodes*."""
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.post(
                    f"{self.url}{node['id']}/gene/increment-recall-threshold",
                    verify=self.secure,
                    headers=self.headers,
                    json={'increment': increment},
                ).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise BottleQueryError(response)
                else:
                    self.genome.primitives[node['id']]['recall_threshold'] += increment
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {"recall_threshold": response['message']}
                result[node['name']] = {"recall_threshold": response['message']}
            except Exception as exception:
                raise BottleQueryError(str(exception)) from None

        return result

    def show_predictions_knowledge_details(self) -> List:
        """ """
        return []

    def start_acting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Allow *nodes* to start acting."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/start', nodes=nodes)

    def stop_acting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Stop *nodes* from acting."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/stop', nodes=nodes)

    def start_sleeping(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to start sleeping."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/start', nodes=nodes)

    def stop_sleeping(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Wakes up sleeping *nodes*."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/stop', nodes=nodes)

    def start_predicting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to start predicting."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'predicting/start', nodes=nodes)

    def stop_predicting(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Tells *nodes* to stop predicting.

        Useful for faster training, but abstracted nodes will not learn.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'predicting/stop', nodes=nodes)

    @_ensure_connected
    def ping(self, nodes: List = None) -> Union[dict, Any]:
        """Ping a node to ensure it's up."""
        if nodes is None:
            return requests.get(f'{self.url}bottle/ping', headers=self.headers).json()
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
            results = {}
            for node in nodes:
                response = requests.get(f"{self.url}{node['id']}/ping", verify=self.secure, headers=self.headers).json()
                if 'error' in response or response["status"] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    print("Failure:", {node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                results[node['name']] = response["message"]
            return results

    @_ensure_connected
    def set_mood(self, mood_data: Dict, nodes: List = None) -> Union[dict, Any]:
        """
        *mood_data* should be of the format:
            {node-name: {emotive-1: value, emotive-2: value}}

        where node-name is the *name* of a primitive or manipulative.
        """
        results = {}
        if nodes is None:
            nodes = [node for node in self.all_nodes]
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        for node in nodes:
            try:
                response = requests.post(
                    f"{self.url}{node['id']}/mood/set", verify=self.secure, headers=self.headers, json={'data': mood_data}
                ).json()
                if 'error' in response or response["status"] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise BottleQueryError(response)
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                results[node['name']] = response["message"]
            except Exception as exception:
                raise BottleQueryError(str(exception)) from None
        return results

    @_ensure_connected
    def analyze_kb(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Kick-starts analysis for the selected primitives' KBs.

        This is a long running process and can be monitored via kb_analysis_progress ('/kb/analysis-progress')
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'kb/analyze', nodes=nodes)

    @_ensure_connected
    def kb_analysis_progress(self):
        """Monitors the KB analysis progress kickstarted by analyze_kb."""
        return requests.get(f'{self.url}kb/analysis-progress', verify=self.secure, json=[], headers=self.headers).json()

    def set_target_class(self, target_class: str, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Provide a target_class symbol for the searcher to look for.

        The searcher will ignore all other classes. This is a symbol that is in the last event of a classification
        sequence.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'set-target-class', nodes=nodes, data=target_class)

    def clear_target_class(self, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Clears target selection."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'clear-target-class', nodes=nodes)


__all__ = (BottleConnectionError, BottleClient, BottleQueryError)
