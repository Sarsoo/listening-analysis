import tensorflow as tf

def ensem_classify(models, test_data, test_labels, round_predictions=True):
    predictions = [model(test_data.to_numpy()) for model in models]
        
    rounded_sum = sum(tf.math.round(pred) for pred in predictions)
    urounded_sum = sum(predictions)
    # round predictions to onehot vectors and sum over all ensemble models
    # take argmax for ensemble predicted class

    correct = 0 # number of correct ensemble predictions
    correct_num_models = 0 # when correctly predicted ensembley, number of models correctly classifying
    individual_accuracy = 0 # proportion of models correctly classifying
    
    classes = list()
     # pc = predicted class, pcr = rounded predicted class, gt = ground truth
    for pc, pcr, gt in zip(urounded_sum, rounded_sum, test_labels):
        gt_argmax = tf.math.argmax(gt)

        if round_predictions:
            pred_val = pcr
        else:
            pred_val = pc
        classes.append(tf.math.argmax(pred_val))
            
        correct_models = pcr[gt_argmax] / len(models) # use rounded value so will divide nicely
        individual_accuracy += correct_models

        if tf.math.argmax(pred_val) == gt_argmax: # ENSEMBLE EVALUATE HERE
            correct += 1
            correct_num_models += correct_models
            
    return classes, predictions, correct / len(test_data), correct_num_models / correct, individual_accuracy / len(test_data)
    