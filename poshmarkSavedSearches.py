import webbrowser
from os import path

searchURL = 'https://poshmark.com/search?query=fjallraven&sort_by=added_desc&my_size=true&department=Men'
# TODO put insid menu class?
searches_dict = {}

def open_search(url: str):
    webbrowser.open(url)

def get_savedsearches():
    searches_dict.clear()
    with open('savedsearches.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                label, url = parts
                searches_dict[label] = url

def list_searches():
    print('Label : Query URL')
    for label in searches_dict:
        print(f'{label} : {searches_dict[label]}\n')

def get_one_search(label):
    if label in searches_dict.keys():
        open_search(searches_dict[label])
        print(f'Opened search {label}')
    else:
        print('Sorry, that search does not exist. Make sure it is typed exactly.')

def get_all_searches():
    for label in searches_dict:
        open_search(searches_dict[label])

def write_txt_from_dict():
    with open('savedsearches.txt', 'w') as file:
        for label, url in searches_dict.items():
            file.write(f'{label},{url}\n')
    get_savedsearches()

def delete_search(label):
    try:
        searches_dict.pop(label)
        print(f'Deleted search {label}')
        write_txt_from_dict()
    except KeyError as e:
        print(f'Could not find saved search "{label}"')

class SearchCreator:

    header = 'https://poshmark.com/search?query='
    women_list = ['Accessories','Bags','Dresses','Intimates & Sleepwear','Jackets & Coats','Jeans','Jewelry','Makeup','Pants & Jumpsuits',
                  'Shoes','Shorts','Skirts','Sweaters','Swim','Tops','Skincare','Hair','Bath & Body','Global & Traditional Wear','None']
    men_list = ['Accessories','Bags','Jackets & Coats','Jeans','Pants','Shirts','Shoes','Shorts','Suits & Blazers','Sweaters','Swim',
                'Underwear & Socks','Grooming','Global & Traditional Wear','None']
    kids_list = ['Accessories','Bottoms','Dresses','Jackets & Coats','Matching Sets','One Pieces','Pajamas','Shirts & Tops','Shoes',
                 'Swim','Costumes','Bath, Skin & Hair','Toys','None']
    home_list = ['Accents','Art','Bath','Bedding','Design','Dining','Games','Holiday','Kitchen','Office','Party Supplies',
                 'Storage & Organization','Wall Decor','None']
    pets_list = ['Dog','Cat','Bird','Fish','Reptile','Small Pets','None']
    none_list = ['None']
    electronics_list = ['Cameras, Photo & Video','Computers, Laptops & Parts','Cell Phones & Accessories','Car Audio, Video & GPS',
                        'Wearables','Tablets & Accessories','Video Games & Consoles','VR, AR & Accessories','Media','Networking',
                        'Headphones','Portable Audio & Video']
    departments_dict = {'Women':women_list,'Men':men_list,'Kids':kids_list,'Home':home_list,'Pets':pets_list,
                        'Electronics':electronics_list,'None':none_list}
    ''' Size Options
    To cover, Women's: Shoes, Dresses, Jeans, pants &jumpsuits, sweaters
    Men's: shoes, pants, shirts, suits & blazers, sweaters
    kids: shoes, bottoms, shirts & tops
    '''
    # size = ()
    color_list = ('Black','White','Orange','Purple','Red','Green','Pink','Blue','Gray','Silver','Yellow','Gold','Brown','Cream','Tan','')
    sort_by_dict = {'Just Shared':'best_match','Just In':'added_desc','Oldest':'added_asc','Price High to Low':'price_desc',
               'Price Low to High':'price_asc','Recently Price Dropped':'price_drop','Likes':'like_count','Relevance':'relevance_v2'}

    def __init__(self):
        pass

    def get_search_query():
        return input('What would you like to search for? You can leave this blank and use other filters instead.\n')

    def get_label_input():
        return input("What would you like to label this search?\n")

    def get_category_input():
        print('Which category would you like to search? Here are your options:')
        options = ''
        for key in SearchCreator.departments_dict.keys():
            options += key +', '
        options = options[:-2]
        print(options)
        while True:
            category = input()
            if category in SearchCreator.departments_dict.keys():
                break
            else:
                print('Sorry, category not recognised. Please type it exactly as in the displayed list. Try again.')
        return category

    def get_sub_category_input(category):
        print('Please select a sub category. Feel free to choose none for a broader search.')
        options = ''
        for item in SearchCreator.departments_dict[category]:
            options += item +', '
        options = options[:-2]
        print(options)
        while True:
            subcategory = input()
            if subcategory in SearchCreator.departments_dict[category]:
                break
            else:
                print('Sorry, category not recognised. Please type it exactly as in the displayed list. Try again.')
        return subcategory

    def get_brand_input():
        brand = []
        while True:
            answer = input('Would you like to add a brand to the search? Answer y/n\n')
            if answer == 'n':
                return brand
            if answer == 'y':
                brand.append(input('What brand would you like to add?\n'))
            else:
                print('Invalid response. Please answer "y" or "n"')
    
    def get_size_input():
        # TODO add a list of options at some point
        size = []
        while True:
            answer = input('Would you like to turn on "My size" filter for this search? Answer y/n\n')
            if answer == 'n':
                break
            if answer == 'y':
                size.append('my_size')
                return size
            else:
                print('Invalid response. Please answer "y" or "n"')

        while True:
            answer = input('Would you like to add a size to the search? Answer y/n\n')
            if answer == 'n':
                return size
            if answer == 'y':
                size.append(input('What size would you like to add?\n'))
            else:
                print('Invalid response. Please answer "y" or "n"')

    def get_color_input():
        color = []
        while True:
            answer = input('Would you like to add a color to the search? Answer y/n\n')
            if answer == 'n':
                return color
            if answer == 'y':
                print('Here are the available options:')
                options = ''
                for c in SearchCreator.color_list:
                    if c == '':
                        continue
                    options += c + ', '
                # TODO test:
                options = options[:-2]
                print(options)
                while True:
                    entry = input('What color would you like to add?\n')
                    if entry in SearchCreator.color_list:
                        color.append(entry)
                        break
                    else:
                        print('Sorry, color not recognised. Try again. Leave blank for none.')
            else:
                print('Invalid response. Please answer "y" or "n"')

    def get_price_input():
        # convert to final format within this method?
        price, min, max = '', '', ''
        while True:
            answer = input('Would you like to add a price range to the search? Answer y/n\n')
            if answer == 'n':
                return price
            if answer == 'y':
                while True:
                    # TODO input verification
                    min = input('What would you like the minimum to be? Enter "0" for none.\n')
                    max = input('What would you like the maximum price limit to be?\n')
                    if type(min) != int or type(max) != int:
                        print('Invalid entry. Make sure max is higher than min, and that only numbers are entered.\n')
                    elif int(max) >= int(min):
                        break
                    print('Invalid entry. Make sure max is higher than min, and that only numbers are entered.\n')
                break
            else:
                print('Invalid response. Please answer "y" or "n"')
        
        combo = min + '-' + max
        if combo == '-':
            return price
        price = '&price[]=' + combo
        return price

    def get_sort_input():
        sort_by, options = '', ''
        print('How would you like the results to be sorted? Here are your options:')
        for key in SearchCreator.sort_by_dict.keys():
            options += key + ', '
        options = options[:-2]
        print(options)
        while True:
            sort_by = input()
            if sort_by in SearchCreator.sort_by_dict.keys():
                break
            else:
                print('Sorry, sort option is not recognised. Please type it exactly as in the displayed list. Try again.')
        sort_by = '&sort_by=' + SearchCreator.sort_by_dict[sort_by]
        return sort_by

    def replace_characters(s):
        # replace spaces w/ _, and & with %26
        s = s.replace(' ', '_')
        s = s.replace('&', '%26')
        return s

    def create_search_from_paste():
        label = input("What would you like to label this search?\n")
        url = input("Please paste the url here.\n")
        searches_dict[label] = url
        write_txt_from_dict()
    
    def create_search_from_user():
        label = SearchCreator.get_label_input()
        query = SearchCreator.get_search_query()
        category = SearchCreator.get_category_input()
        sub_category = SearchCreator.get_sub_category_input(category)
        brand = SearchCreator.get_brand_input()
        size = SearchCreator.get_size_input()
        color = SearchCreator.get_color_input()
        price = SearchCreator.get_price_input()
        sort_by = SearchCreator.get_sort_input()
        # TODO test:
        
        SearchCreator.build_new_search(label, query, category, sub_category, brand, size, color, price, sort_by)

    def build_new_search(label: str, query: str, category: str, sub_category: str, brand: list, size: list, color: list, price: str, sort_by: str):
        # Convert and clean/modify user input
        # category
        sub_category = SearchCreator.replace_characters(sub_category)        
        category = f'&department={category}&category={sub_category}'
        # brand
        brand_str = ''
        for b in brand:
            brand_str += f'&brand[]={b}'
        # TODO size conversion
        size_str = ''
        if size[0] == 'my_size':
            size_str = '&my_size=true'
        else:    
            for s in size:
                size_str += f'&size[]={s}'
        # color
        color_str = ''
        for c in color:
            color_str += f'&color[]={c}'
        # price and sort already done
        # Build actual url, and save to .txt
        url = SearchCreator.header + query + category + brand_str + size_str + color_str + price + sort_by
        print(url)
        searches_dict[label] = url
        write_txt_from_dict()
    
class Menu:

    def __init__(self):
        # make sure text file exists, and load data to dict
        if not path.isfile('savedsearches.txt'):
            with open('savedsearches.txt', 'x'):
                pass
        get_savedsearches()
    
    def print_menu(self):
        title = 'Poshmark Search Saver'
        instructions = 'Please type the number of the option you want.'
        option_1 = '    1. List all saved searches.'
        option_2 = '    2. Open all saved searches in browser.'
        option_3 = '    3. Open specific search in browser.'
        option_4 = '    4. Create new search.'
        option_5 = '    5. Create new search from paste.'
        option_6 = '    6. Delete search.'
        option_7 = '    7. Quit.'
        print()
        print(title)
        print(instructions)
        print(option_1)
        print(option_2)
        print(option_3)
        print(option_4)
        print(option_5)
        print(option_6)
        print(option_7)
        print()

    def select_choice(self, selection):
        # TODO input verification on all

        if selection == '1':
            list_searches()
            input('Press enter to return to menu.')
        if selection == '2':
            get_all_searches()
            input('Searches opened. Press enter to return to menu.')
        if selection == '3':
            s = input('Which search would you like to open in the browser? Make sure label is an exact match.\n')
            get_one_search(s)
            input('Press enter to return to menu.')
        if selection == '4':
            SearchCreator.create_search_from_user()
            input('Search created. Press enter to return to menu.')
        if selection == '5':
            SearchCreator.create_search_from_paste()
            input('Search created. Press enter to return to menu.')
        if selection == '6':
            s = input('Which search would you like to delete? Make sure the label is an exact match.\n')
            delete_search(s)
            # TODO only print if actually deleted something
            input('Press enter to return to menu.')
        pass
    
    def run_menu(self):
        while True:
            self.print_menu()
            selection = input()
            if selection not in ['1', '2', '3', '4', '5', '6', '7']:
                print('Invalid selection. Please try again.')
                continue
            if selection == '7':
                break
            else:
                self.select_choice(selection)

if __name__ == "__main__":
    menu = Menu()
    menu.run_menu()