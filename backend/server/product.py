import sys

'''
Wine object for east using and saving data 
'''



class Product:
    def __init__(self, product_id, name, input_prices):
        self.id = product_id
        self.name = name
        self.prices = {}
        self.set_prices( input_prices)
        
    def __str__(self):
        prices_str = ""
        for store in self.prices:
            prices_str += f"{store}\nregular_price --> {self.prices[store]['regular_price']} \nclub_price --> {self.prices[store]['club_price']}\nsale_price --> {self.prices[store]['sale_price']}\n\n"
            minP = self.min_price()
        return (f"\nProduct ID: {self.id}, Name: {self.name}\nPrice:\n${prices_str}\nmin_price: {minP}\n")
    
    def min_price(self):
        min_res = sys.maxsize
        store_res = ""        
        for store in self.prices:
            if self.prices[store]["regular_price"] < min_res and self.prices[store]["regular_price"] > 0:
                min_res = self.prices[store]["regular_price"]
                store_res = store
            if self.prices[store]["club_price"] < min_res and self.prices[store]["club_price"] > 0  :
                min_res = self.prices[store]["club_price"]
                store_res = store
            
        return (store_res , min_res)
        
    def set_prices(self, input_prices):
        for store in input_prices:
            self.prices[store] = {"regular_price" : float(input_prices[store]["regular_price"]) ,
                                          "club_price" : float(input_prices[store]["club_price"]) , 
                                          "sale_price" : input_prices[store]["sale_price"]}
            
