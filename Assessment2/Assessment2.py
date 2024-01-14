# IMPORTING NECESSARY LIBRARIES
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io

# a class to represents the main application
# this is to initializes the GUI and help in defining methods for handling data
class Drinks:
    #setting up the main window of the application
    def __init__(self, root):
        self.root = root
        self.root.title("drinks!")
        self.root.geometry("1095x750")
        self.root.resizable(False,False)

# MADE MY  BACKGROUND IMAGE ON FIGMA || slice the image for 2 frames
        # Left Frame ------------------------------------
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # HANDLING BACKGROUND IMAGE FOR BOTH OF THE FRAME
        bg_image = Image.open(r"ADV_PROG_AS2\Assessment2\bg1.png")  #Path
        bg_image = bg_image.resize((642, 729)) # size
        bg_photo = ImageTk.PhotoImage(bg_image) # variable to display

        # a label to display the background image
        bg_label = tk.Label(left_frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        bg_image1 = Image.open(r"ADV_PROG_AS2\Assessment2\bg2.png") # RIGHT FRAME IMG
        bg_photo1 = ImageTk.PhotoImage(bg_image1)

        # Right Frame
        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1,sticky="nsew")

        bg_label1 = tk.Label(right_frame, image=bg_photo1)
        bg_label1.image = bg_photo1
        bg_label1.place(relx=0, rely=0, relwidth=1, relheight=1)

    # A Description label -------------------------------------------------------
        self.description_label = ttk.Label(left_frame, text="1. Search a drink/Select a Category. Then press the search button",
                                           font=("Helvetica", 10))

        # Entry for searching cocktails
        self.search_entry = ttk.Entry(left_frame, width=30)#Can be Updated by users

        # Combobox for selecting category
        self.category_combobox = ttk.Combobox(left_frame, values=self.get_categories())#Values used to display item in combobox
        self.category_combobox.set("Select Category")

        # Button to trigger search
        search_button = ttk.Button(left_frame, text="Search", command=self.search_cocktails)

        # A Description label
        self.description2_label = ttk.Label(left_frame, text="2. Search Item from the list",
                                           font=("Helvetica", 10))
        # Listbox to display search results
        self.results_listbox = tk.Listbox(left_frame, height=10, selectmode=tk.SINGLE)# allowing only to select one

        # A Description label
        self.description3_label = ttk.Label(left_frame, text="3. Click view Button",
                                           font=("Helvetica", 10))

        # Button to view details of the selected cocktail
        view_button = ttk.Button(left_frame, text="View Details", command=self.view_details)

        # A Description label
        self.description4_label = ttk.Label(left_frame, text="Generate random drink!",
                                           font=("Helvetica", 10))

        # Button for a random cocktail
        random_button = ttk.Button(left_frame, text="Random Cocktail", command=self.get_random_cocktail)

        # Text widget to display details
        self.details_text = tk.Text(right_frame, wrap="word", width=40, height=12, font=("Helvetica", 10))

        # Image display 
        self.cocktail_image_label = tk.Label(right_frame)

        # Positioning for widgets in left frame
        self.description_label.grid(row=1, column=0, columnspan=3, padx=50, pady=(140, 0))
        self.search_entry.grid(row=2, column=0, padx=10, columnspan=3, pady=6)
        self.category_combobox.grid(row=3, column=0, columnspan=3, padx=10, pady=6)
        self.description2_label.grid(row=4, column=0, columnspan=3, pady=6)
        search_button.grid(row=5, column=0, columnspan=3, padx=10, pady=6)
        self.results_listbox.grid(row=6, column=0, columnspan=3, padx=10, pady=6)
        self.description3_label.grid(row=7, column=0, columnspan=3, pady=6)
        view_button.grid(row=8, column=1, columnspan=1, padx=10, pady=6)
        self.description4_label.grid(row=9, column=0, columnspan=3, pady=6)
        random_button.grid(row=10, column=1, columnspan=1, padx=10, pady=6)

        # Positioning for widgets in right frame
        self.cocktail_image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(110, 10))
        self.details_text.grid(row=1, column=0, columnspan=3, padx=10, pady=0)

        # Adjusting row and column weights to make frames expandable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        
        #Style to match background color
        style = ttk.Style()
        style.configure("Bg.TLabel", background="#43414A")  # Set the background color

        # Applying the style to the label
        self.description_label["style"] = "Bg.TLabel"
        self.description2_label["style"] = "Bg.TLabel"
        self.description3_label["style"] = "Bg.TLabel"
        self.description4_label["style"] = "Bg.TLabel"

#FUNCTION TO USE AS COMMANDS AND VALUES ----------------------------------------------------------
    # FOR GETTING CATEGORY FROM API AND DISPLAYING IT
    def get_categories(self):
        # Fetching the list of categories from the API
        category_url = "https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list" #API USED
        response = requests.get(category_url) # GETTING REQUEST 
        data = response.json() # OBTAINING RESPONSE

        # Checks if there are drink categories available in the API response/data
        if data['drinks']:
            categories = [category['strCategory'] for category in data['drinks']]
            return ["Select Category"] + categories # DISPLAYS CATEGORY IN COMBOBOX
        else:
            return ["Select Category"]
    
    # FOR SEARCH BUTTON FUNCTION
    def search_cocktails(self):
        # GETTING USERS INPUT AND STORING IT IN A VARIABLE
        query = self.search_entry.get() 
        category = self.category_combobox.get()

        if query and category == "Select Category": # if there is no chosen category
            # Searching user input in API. Search by query
            # Same fetch approach
            search_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={query}"
            response = requests.get(search_url)
            data = response.json()
            
            
            self.results_listbox.delete(0, tk.END)  # Responsible for clearing previous results

            if data['drinks']:# if drinks is found
                for drink in data['drinks']: # ITERATES LIST
                    self.results_listbox.insert(tk.END, drink['strDrink'])# insert in listbox
                
                # Display the image of the first result (if available)
                self.display_cocktail_image(data['drinks'][0]['strDrinkThumb'])
            else: # If drinks not found
                self.results_listbox.insert(tk.END, "No results found.")
                
        # IF THERE IS A SELECTED CATEGORY       
        elif category != "Select Category":
            # Search by category
            search_url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?c={category}"
            response = requests.get(search_url)
            data = response.json()

            self.results_listbox.delete(0, tk.END)  # Clear previous results

        #SAME APPROACH
            if data['drinks']:
                for drink in data['drinks']:
                    self.results_listbox.insert(tk.END, drink['strDrink'])
                
                # Display the image of the first result (if available)
                self.display_cocktail_image(data['drinks'][0]['strDrinkThumb'])
            else:
                self.results_listbox.insert(tk.END, "No results found.")
        else:
            messagebox.showwarning("Input Required", "Please enter a query or select a category.")
            
    # TO DISPLAY INFO ABOUT DRINK FROM strDrink-strCategory-strGlass-strGlass-strInstruction
    def view_details(self):
        #Curselection for single selection
        selected_index = self.results_listbox.curselection() # Retrieves the index of the currently selected item in the results_listbox
        if selected_index: # Checks if there is a selected item
            # Retrieves the name of the selected drink from the listbox using the selected index
            selected_drink = self.results_listbox.get(selected_index)
            
            #FETCHING || SEARCHING BY SELECTED_DRINKS
            details_url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={selected_drink}"
            response = requests.get(details_url)
            data = response.json()

            if data['drinks']: # If API found data about selected drinks 
                drink_details = data['drinks'][0]# Retrieves the details of the selected drink from the first item
                # Variable to store details to be displayed
                details_text = f"Name: {drink_details['strDrink']}\n" \
                               f"Category: {drink_details['strCategory']}\n" \
                               f"Glass Type: {drink_details['strGlass']}\n" \
                               f"Instructions: {drink_details['strInstructions']}\n" \
                               f"Ingredients: {self.get_ingredients(drink_details)}"
              
                self.details_text.delete(1.0, tk.END)  # Clear previous details
                self.details_text.insert(tk.END, details_text) # Displays details

                # Display the image of the selected drink
                self.display_cocktail_image(drink_details['strDrinkThumb'])

    # FOR RANDOM BUTTON FUNCTION
    def get_random_cocktail(self):
        random_url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        response = requests.get(random_url)
        data = response.json()

        # DISPLAYING INFO AND IMAGE OF A RANDOM DRINK
        if data['drinks']:
            random_drink = data['drinks'][0]
            details_text = f"Name: {random_drink['strDrink']}\n" \
                           f"Category: {random_drink['strCategory']}\n" \
                           f"Glass Type: {random_drink['strGlass']}\n" \
                           f"Instructions: {random_drink['strInstructions']}\n" \
                           f"Ingredients: {self.get_ingredients(random_drink)}"

            self.details_text.delete(1.0, tk.END)  # Clear previous details
            self.details_text.insert(tk.END, details_text)

            # Display the image of the random drink
            self.display_cocktail_image(random_drink['strDrinkThumb'])
    
    # FOR GETTING INGREDIENTS DETAILS      
    def get_ingredients(self, drink_details): # PARAMETER drink_details will be used
        ingredients = [] # Empty list to be used to add in items
        for i in range(1, 16): # Iteration || assuming that the ingredients and measurements are indexed with numbers in the API response
            ingredient_key = f"strIngredient{i}" # Getting all ingredients
            measure_key = f"strMeasure{i}" # Getting all measurements
            if drink_details[ingredient_key]: # if there is an ingredients
            #variables for displaying
                ingredient = drink_details[ingredient_key]
                #If there is no measurement provided  it defaults to the string "as needed."
                measure = drink_details[measure_key] if drink_details[measure_key] else "as needed"
                ingredients.append(f"{ingredient} ({measure})")  # Appending to the ingredients list
        # Joins the list of formatted ingredients into a single string using newline characters ("\n") 
        return "\n".join(ingredients)

    #FOR DISPLAYING IMAGE OF COCKTAIL CHOSEN
    def display_cocktail_image(self, image_url): #Parameter image_url that dynamically obtained from the API response
        # GETTING IMAGE FOR FROM API
        response = requests.get(image_url)
        img_data = response.content
        
        # USING PIL TO LOAD IMAGE 
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((200, 200))  # Resize the image
        img = ImageTk.PhotoImage(img) # CONVERTS TO TKINTER OBJECT

        # Updating the image label for display
        self.cocktail_image_label.config(image=img)
        self.cocktail_image_label.image = img

# FINALLY DISPLAY GUI!!
if __name__ == "__main__":
    root = tk.Tk()
    app = Drinks(root)
    root.mainloop()