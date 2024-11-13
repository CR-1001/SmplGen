# This file is part of SmplGen. Copyright (C) 2024 Christian Rauch.
# Distributed under terms of the GPL3 license.


import datetime
import random
import string
import math

import pandas as pd


class Common:

    def s(v)        -> str:   return str(v)
    def str(v)      -> str:   return str(v)
    def i(v)        -> int:   return int(v)
    def int(v)      -> int:   return int(v)
    def f(v)        -> float: return float(v)
    def float(v)    -> float: return float(v)
    def exp(v)      -> float: return math.exp(v)
    def abs(v)      -> float: return abs(v)
    def round(v, p) -> float: return round(v, p)
    def min(v, v2)  -> float: return min(v, v2)
    def max(v, v2)  -> float: return max(v, v2)

    calls = 0
    def count() -> int:
        c = Common.calls
        Common.calls += 1
        return c
    
    states = {}
    def state(key, value, return_value=True): 
        Common.states[key] = value
        return value if return_value else ""

    def state(key, fallback=""): 
        if key not in Common.states: return fallback
        return Common.states[key]

    def set(count: int, distrfunc: callable, distrfunc_args: tuple, separator: str=',', start: str='{', end: str='}', sort_desc: bool=True):
        values = set()
        while len(values) < count:
            value = distrfunc(*distrfunc_args)
            values.add(value)
        values = [str(v) for v in sorted(list(values), reverse=sort_desc)]
        values_str = separator.join(values)
        return f"{start}{values_str}{end}"
    
    def csv(file: str, head=None, rows=None) -> pd.DataFrame:
        template = CsvTemplate(file, head, rows)
        return template
    

class CsvTemplate:
    def __init__(self, file: str, head=None, rows=None) -> str:
        self.df = pd.read_csv(file, header=head, nrows=rows)

    def col(self, index: int):
        return self.df.iloc[:,index]
    
    def row(self, index: int):
        return self.df.iloc[index,:]


class Interval:

    def interval(min: int, max: int, length: int, separator: str=' '):
        st = int(random.uniform(min, max - length))
        end = st + length
        return f'{int(st)}{separator}{int(end)}'

    def intervalp(min: int, max: int, length_percent: float, separator: str=' '):
        length = (max - min) / length_percent
        return Interval.interval(min, max, length, separator)
    

class People:

    def first_name():
        return random.choice(
            ["Muhammad", "Sofia", "Aisha", "Liam", "Aarav", "Emma", 
            "Noah", "Ava", "Adebayo", "Chen", "Lucas", "Isabella", 
            "Mateo", "Mia", "Ethan", "Kofi", "Amelia", "Alexander", 
            "Wei", "Olivia", "Benjamin", "Chloe", "Elijah", "Aiden", 
            "Charlotte", "Daniel", "Zayn", "Lily", "Leo", "Aria", 
            "Yusuf", "Hannah", "Ali", "Mila", "Oscar", "Sophie", ])
    
    def last_name():
        return random.choice(
            ["Singh", "Wang", "Nguyen", "Smith", "Kumar", "Zhang", 
            "Garcia", "Kim", "Olu", "Chen", "Müller", "Ahmed", 
            "Brown", "Patel", "Lopez", "Hussein", "Lee", "Hernandez", 
            "Mohamed", "Davies", "Taylor", "Martinez", "Robinson", 
            "Olamide", "Thompson", "Silva", "Clark", "Rodriguez", 
            "Chow", "Baker", "Martin", "Scott", "Cissé", "Adams", 
            "Zhou", "Torres"])
    
    def user(rndfunc_letters = None):
        if rndfunc_letters == None:
            rndfunc_letters = random.randint(6, 12)
        letters = string.ascii_letters + string.digits
        username = ''.join(random.choice(letters) for i in range(rndfunc_letters))
        return username
    
    def day(start_year=None, end_year=None):
        if start_year is None:
            start_year = datetime.datetime.now().year - 100
        if end_year is None:
            end_year = datetime.datetime.now().year - 18

        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date.strftime("%Y-%m-%d")
    
    def email():
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]
        domain = random.choice(domains)
        
        letters = string.ascii_letters + string.digits
        username = ''.join(random.choice(letters) for i in range(random.randint(5, 10)))
        
        return f"{username}@{domain}"
    

class TempInfRet:

    dat_cache = dict()
    dat_interval_cache = dict()

    def tir_query(dat_file: str, elements_count: int, extent_percent: float, min_elem_id: int=None, max_elem_id: int=None):
        extent_percent = extent_percent / 100
        # cache values
        if dat_file not in TempInfRet.dat_cache:
            template = pd.read_csv(dat_file, sep="\\s+", header=None)
            template.columns = ['start', 'end', 'elements']
            gstart   = template.iloc[:,0].min()
            gend     = template.iloc[:,1].max()
            TempInfRet.dat_cache[dat_file]          = template
            TempInfRet.dat_interval_cache[dat_file] = (gstart, gend)
        template     = TempInfRet.dat_cache[dat_file]
        gstart, gend = TempInfRet.dat_interval_cache[dat_file]
        domain = gend - gstart
        extent = int(domain * extent_percent)
        while True:
            row      = template.sample(1).iloc[0]
            rstart   = int(row.iloc[0])
            rend     = int(row.iloc[1])
            elements = str(row.iloc[2]).split(',')
            if min_elem_id != None:
                elements = [str(e) for e in elements if int(e) >= min_elem_id]
            if max_elem_id != None:
                elements = [str(e) for e in elements if int(e) <= max_elem_id]
            if len(elements) >= elements_count:
                elements_sample = random.sample(elements, elements_count)
                elements_sample = sorted([int(e) for e in elements_sample], reverse=True)
                elements_str    = ",".join([str(e) for e in elements_sample])
                qstart_max      = rend
                qstart_min      = rstart - extent
                qstart          = int(random.uniform(qstart_min, qstart_max))
                qend            = qstart + extent
                if qend > gend or qstart < gstart: continue
                r_str = f"{str(rstart).ljust(10)} {str(rend).ljust(10)} {row.iloc[2]}"
                q_str = f"{str(qstart).ljust(10)} {str(qend).ljust(10)} {elements_str}"
                #print(f"{r_str}\n{q_str}\n----------")
                return q_str

        

