
""" This is the demographics Class. It contains all of the Demographic Information of
the inbox Owner. If a value does not apply to the inbox Owner it should be defaulted as a None. """


class Demographics(object):
    # -- Methods
    def __init__(self, firstname, lastname, email, phone_number, gender, ethnicity,
                 age, birth_date, birthplace, country, affiliation):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number
        self.gender = gender
        self.ethnicity = ethnicity
        self.age = age
        self.birth_date = birth_date
        self.birthplace = birthplace
        self.country = country
        self.political_affiliation = affiliation


class BirthplaceUS(object):
    # -- Methods
    def __init__(self, city, state):
        self.city = city
        self.state = state


class BirthplaceInt(object):
    # -- Methods
    def __init__(self, city, country):
        self.city = city
        self.country = country
