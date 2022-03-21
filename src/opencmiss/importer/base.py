import os.path


def valid(inputs, description):
    if type(inputs) != type(description):
        return False

    if len(inputs) != len(description):
        return False

    if type(inputs) == list:
        for index, input_ in enumerate(inputs):
            if "mimetype" in description[index]:
                if not os.path.isfile(input_):
                    return False

    return True
