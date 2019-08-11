def choice_creation(choices_name):
    choices_list = []
    for cat in choices_name:
        choices_list.append(tuple([cat,cat]))
    return choices_list