class HashTable:

    def __init__(self, table_size):         # can add additional attributes
        self.table_size = table_size        # initial table size
        self.hash_table = [None]*self.table_size# hash table
        self.num_items = 0                  # empty hash table

    def insert(self, key, value):
        """ Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value is any object (e.g. Python List).
        If the key is not already in the table, the key is inserted along with the associated value
        If the key is is in the table, the new value replaces the existing value.
        When used with the concordance, value is a Python List of line numbers.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased (doubled + 1)."""
        ind=self.horner_hash(key)
        sind=ind
        add=1

        while True: 
            c_ind=ind%self.table_size
            if self.hash_table[c_ind] is None:
                self.hash_table[c_ind]=[key,value,sind]
                self.num_items+=1
                break
            if self.hash_table[c_ind][0]==key:
                self.hash_table[c_ind][1]=value
                break
            ind+=add
            add+=2

        if self.get_load_factor()>0.5:
            self.num_items=0
            self.table_size<<=1
            self.table_size+=1

            nlist = [pair for pair in self.hash_table if pair is not None]
            self.hash_table=[None]*self.table_size 

            for pair in nlist:
                nind=pair[2]
                nadd=1
                while True: 
                    nc_ind=nind%self.table_size
                    if self.hash_table[nc_ind] is None:
                        self.hash_table[nc_ind]=pair
                        self.num_items+=1
                        break
                    nind+=nadd
                    nadd+=2

    def horner_hash(self, key):
        """ Compute and return an integer from 0 to the (size of the hash table) - 1
        Compute the hash value by using Horner’s rule, as described in project specification."""
        #TODO does not return value between 1 and length of hash table, this is by design -> allows for faster rehashing
        myhash=ord(key[len(key)-1])
        for i in range(len(key)-1, 0, -1):
            myhash=ord(key[i-1])+31*myhash
        return myhash


    def in_table(self, key):
        """ Returns True if key is in an entry of the hash table, False otherwise. Must be O(1)."""
        ind=self.horner_hash(key)
        add=1

        while True:
            c_ind=ind%self.table_size
            if self.hash_table[c_ind] is None:
                return False
            if self.hash_table[c_ind][0]==key: 
                return True
            ind+=add
            add+=2

    def get_index(self, key):
        """ Returns the index of the hash table entry containing the provided key. 
        If there is not an entry with the provided key, returns None. Must be O(1)."""
        ind=self.horner_hash(key)
        add=1

        while True: 
            c_ind=ind%self.table_size
            if self.hash_table[c_ind] is None: 
                return
            if self.hash_table[c_ind][0]==key: 
                return c_ind 
            ind+=add
            add+=2

    def get_all_keys(self):
        """ Returns a Python list of all keys in the hash table."""
        return [pair[0] for pair in self.hash_table if pair is not None]

    def get_value(self, key):
        """ Returns the value (for concordance, list of line numbers) associated with the key.
        If key is not in hash table, returns None. Must be O(1)."""
        ind=self.horner_hash(key)
        add=1

        while True: 
            c_ind=ind%self.table_size
            if self.hash_table[c_ind] is None: 
                return
            if self.hash_table[c_ind][0] == key: 
                return self.hash_table[c_ind][1]
            ind+=add
            add+=2

    def get_num_items(self):
        """ Returns the number of entries (words) in the table. Must be O(1)."""
        return self.num_items

    def get_table_size(self):
        """ Returns the size of the hash table."""
        return self.table_size

    def get_load_factor(self):
        """ Returns the load factor of the hash table (entries / table_size)."""
        return self.num_items/self.table_size
