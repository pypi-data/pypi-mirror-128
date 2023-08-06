"""Implements a variety of prediction models."""
from collections import Counter


def prediction_ensemble_model_utility(ensemble):
    """Using a Weighted Moving Average, though the 'moving' part refers to the prediction index."""
    # using a weighted posterior_probability = potential/marginal_probability
    # FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    if ensemble:
        principal_value = ensemble[0]['utility']
        # Let's use the "best" match as our starting point. Alternatively, we can use,say, the
        # average of all values before adjusting.
        marginal_probability = sum([x['potential'] for x in ensemble])
        result = principal_value + (
            sum([(x['utility'] - principal_value) * (x['potential']) for x in ensemble[1:]])) / marginal_probability
        if result != 0:
            return result
    return None


def prediction_ensemble_model_classification(ensemble):
    """For classifications, we don't bother with marginal_probability because classifications are discrete symbols, not numeric values."""
    boosted_prediction_classes = Counter()
    for prediction in ensemble:
        for symbol in prediction['future'][-1]:
            if "|" in symbol:
                symbol = symbol.split("|")[-1]  # grab the value, remove the piped keys
            boosted_prediction_classes[symbol] += prediction['potential']
    if len(boosted_prediction_classes) > 0:
        return boosted_prediction_classes.most_common(1)[0][0]
    else:
        return None


def prediction_ensemble_model_emotives(ensemble):
    """Calculate a single set of emotive values that model the set of emotives in the ensemble."""
    if ensemble:
        emotives_set = []
        principal_emotives = {}
        for ekey in [prediction['emotives'].keys() for prediction in ensemble]:
            emotives_set += list(ekey)
        new_emotives = {key: None for key in set(emotives_set) }
        marginal_probability = sum([prediction['potential'] for prediction in ensemble])
        for j, prediction in enumerate(ensemble):
            for emotive, v in prediction['emotives'].items():
                if new_emotives[emotive] is None:
                    new_emotives[emotive] = v
                    principal_emotives[emotive] = (v, j) ## this is now the principle_emotive and the prediction from which it came
        for emotive, p_j in principal_emotives.items():
            principle_emotive, j = p_j
            value = sum([((x['emotives'][emotive] - principle_emotive)/principle_emotive) * x['potential'] for x in ensemble[j:] if emotive in x['emotives']]) / marginal_probability
            new_emotives[emotive] += value
        return new_emotives


def hive_model_utility(ensembles):
    """Average of final node predictions."""
    if ensembles:
        modeled_utilities = [prediction_models.prediction_ensemble_model_utility(p) for p in ensembles.values() ]
        prediction = [u for u in modeled_utilities if (u != 0 and u is not None)]
        if prediction:
            return sum(prediction) / len(prediction)
    return None


def hive_model_classification(ensembles):
    """Every node gets a vote."""
    if ensembles:
        # This just takes the first "most common", even if there are multiple that have the same frequency.
        boosted_classifications = [prediction_ensemble_model_classification(c) for c in ensembles.values()]
        votes = Counter([p for p in boosted_classifications if p is not None]).most_common()
        if votes:
            return votes[0][0]
    return None

