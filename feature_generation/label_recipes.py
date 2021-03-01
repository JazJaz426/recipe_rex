import ast
import numpy as np
import pandas as pd
    
def label_meat(ing, include, exclude):    
    for i_ in ing:
        i_ = i_.lower()
        # check if any meats are present in ingredient
        for meat in include:
            if meat in i_:
                # check if all excluded terms are not present too
                if all([e not in i_ for e in exclude]):
                    return 1
    return 0

def label_all_meats(ing):
    poultry = ['chicken', 'turkey', 'duck', 'quail', 'thigh', 'breast']
    beef = ['beef', 'steak', 'ribeye', 'sirloin', 'oxtail', 'brisket', 'bison', 'dog', 'gyoza']
    pork = ['pork', 'bacon', 'ham', 'sausage', 'dog', 'spam', 'rib', 'pastrami', 'prosciutto']
    fish = ['fish', 'tilapia', 'salmon', 'cod', 'flounder', 'shrimp', 'tuna', 'sardine', 'barramundi', 'branzino', 'porgies', 'bass']
    seafood = ['octopus', 'oysters', 'clam', 'abalone', 'squid', 'calamari', 'seafood', 'crab', 'lobster', 'mussel', 'scallop', 'snail']
    lamb = ['lamb']
    exclude = ['chicken stock', 'fish sauce']
    
    poultry_ = label_meat(ing, poultry, exclude)
    beef_ = label_meat(ing, beef, exclude)
    pork_ = label_meat(ing, pork, exclude)
    fish_ = label_meat(ing, fish, exclude)
    seafood_ = label_meat(ing, seafood, exclude)
    lamb_ = label_meat(ing, lamb, exclude)
    labels = [poultry_, beef_, pork_, fish_, seafood_, lamb_]
    
    # vegeterian is not any
    veg = int(not any(labels))
    labels.append(veg)
    return labels

def get_meat_labels(main_recipes, save = False):
#     main_recipes = pd.read_csv('../clean_data/mains_filter_recipes_nutrient.csv')
    main_ing = main_recipes['ingredients'].apply(ast.literal_eval)

    label_names = ['poultry', 'beef', 'pork', 'fish', 'seafood', 'lamb', 'veg']

    # start_index, last_index = 0, 2000
    # for i, (title, ing) in enumerate(zip(main_recipes['title'][start_index:last_index], main_ing[start_index:last_index])):
    #     labels = label_all_meats(ing)
    #     if labels[-1] == 1:
    #         print(i, label_all_meats(ing), title)

    meat_labels = []
    for ing in main_ing:
        meat_labels.append(label_all_meats(ing))

    meat_labels = np.array(meat_labels)
    meat_label_df = pd.DataFrame(meat_labels, index = main_recipes['url'], columns = label_names)
    
    if save:
        print('saving to clean_data/mains/meat_label.csv\n')
        meat_label_df.to_csv('../clean_data/mains/meat_labels.csv')

    return meat_label_df

def label_starch(ing, include, exclude):    
    for i_ in ing:
        i_ = i_.lower()
        # check if any meats are present in ingredient
        for meat in include:
            if meat in i_:
                # check if all excluded terms are not present too
                if all([e not in i_ for e in exclude]):
                    return 1
    return 0

def label_soup(ing, title):
    soup = ['cups chicken broth', 'cups vegetable stock', 'cups chicken stock']
    soup_ = label_starch(ing, soup, [])
    if soup_ or ('soup' in title.lower() and 'soup dumpling' not in title.lower()):
        return 1
    return 0

def label_salad(ing, title):
    if 'salad' in title.lower():
        return 1
    return 0

def label_wrap(ing, title):
    if 'wrap' in title.lower() and 'wrapped' not in title.lower() and 'wonton wrap' not in title.lower() and 'wrapper' not in title.lower() :
        return 1
    return 0

def label_stirfry(ing, title):
    if 'stir fry' in title.lower():
        return 1
    return 0
    
def label_all_starches(ing, title):
    noodle = ['noodle', 'vermicelli']
    rice = ['rice']
    stew = ['curry', 'stew', 'garam masala']
    exclude = ['rice wine', 'rice vinegar', 'rice powder', 'rice noodle', 'vermicelli']
    
    noodle_ = label_starch(ing, noodle, [])
    rice_ = label_starch(ing, rice, exclude)
    soup_ = label_soup(ing, title)
    stew_ = label_starch(ing, stew, exclude)
    salad_ = label_salad(ing, title)
    wrap_ = label_wrap(ing, title)
    stir_fry_ = label_stirfry(ing, title)
    labels = [noodle_, rice_, soup_, stew_, salad_, wrap_, stir_fry_]
    
    return labels

def get_starch_labels(main_recipes, save = False):
#     main_recipes = pd.read_csv('../clean_data/mains_filter_recipes_nutrient.csv')
    main_ing = main_recipes['ingredients'].apply(ast.literal_eval)

    label_names = ['noodle', 'rice', 'soup', 'stew', 'salad', 'wrap', 'stir_fry']
    print(label_names)

#     start_index, last_index = 0, 2000
#     for i, (title, ing) in enumerate(zip(main_recipes['title'][start_index:last_index], main_ing[start_index:last_index])):
#         labels = label_all_starches(ing, title)
# #         if labels[-2] == 1 and 'soup' not in title.lower():
#         print(i, labels, title)

    starch_labels = []
    for title, ing in zip(main_recipes['title'], main_ing):
        starch_labels.append(label_all_starches(ing, title))

    starch_labels = np.array(starch_labels)
    starch_labels_df = pd.DataFrame(starch_labels, index = main_recipes['url'], columns = label_names)
    
    if save:
        print('saving to clean_data/mains/starch_label.csv\n')
        starch_labels_df.to_csv('../clean_data/mains/starch_labels.csv')

    return starch_labels_df