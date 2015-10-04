import argparse
import collections
import json
import re
import itertools
import operator

class Rolodex():
    def __init__(self, input_lines= []):
        self.input_lines= input_lines
        self.error_lines= []
        self.rolo_entries= []

        self.types= {'type1': ('lastname', 'firstname', 'phonenumber', 'color', 'zipcode'),
                     'type2': ('firstname', 'lastname', 'color', 'zipcode', 'phonenumber'),
                     'type3': ('firstname', 'lastname', 'zipcode', 'phonenumber', 'color'),
                     'typeo': ('color', 'firstname', 'lastname', 'phonenumber', 'zipcode'),
                     }

    @staticmethod
    def is_numeric(arg):
        try:
            t= int(str(arg))
            return(True)
        except:
            return(False)

    def phone_normalize(self, phone):
        p= re.sub("[^0-9]", "", phone)
        if len(p) != 10:
            return ""
        return "%s-%s-%s" % (p[0:3], p[3:6], p[6:])

#  entries in the rolodex list may fall into one of three different types.
#    type 1: lastname, firstname, phone, color, zip
#    type 2: firstname lastname, color, zip, phone
#    type 3: firstname, lastname, zip, phone, color
#
#  this method takes a line and returns a dict of
#    {'firstname': v0, 'lastname': v1, 'color': v2, 'zipcode': v3, 'phonenumber': v4}
# or an empty dict if the input line coud not be parsed
    def parse(self, rolo_line= ""):
        s_list= [str(elem).strip() for elem in rolo_line.split(',')]

        if len(s_list) == 4:
            #  if the split list has four elements then it is type2.
            #  split the first element on ' ' and flatten the list
            cur_type= 'type2'
            s_list= [i for i in s_list[0].split(' ')] + s_list[1:]
        elif len(s_list) == 5:
            # if the list has 5 elements it might be type1 or type3
            cur_type= 'type1' if Rolodex.is_numeric(s_list[4]) else 'type3'
        else:
            # if the list does not have 4 elements or 5 elements, it
            # is an error line
            return({})

        # mak a dict and then normalize the phone number.  if it
        # cannot be normalized then return an error (empty dict)
        d= dict(zip(self.types[cur_type], s_list))
        d['phonenumber']= self.phone_normalize(d['phonenumber'])
        if len(d['phonenumber']) == 0:
            return({})

        # put the results in an ordered dict to match the spec
        return(collections.OrderedDict([(i, d[i]) for i in self.types['typeo']]))


    def run(self):
        for i, l in enumerate(self.input_lines):
            d= self.parse(l)
            if len(d.keys()) == 0:
                self.error_lines.append(i)
            else:
                self.rolo_entries.append(d)

        self.rolo_entries.sort(key= operator.itemgetter('lastname', 'firstname'))
        out= collections.OrderedDict([('entries', self.rolo_entries), ('errors', self.error_lines)])
        return json.dumps(out, indent=4, separators=(',', ': '))

if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='rolodex', description='Examine a list of names and addresses.')
    parser.add_argument('rolodex_file', nargs=1, help='Names and Addresses')
    args = parser.parse_args()

    data = [line.strip() for line in open(args.rolodex_file[0])]

    r= Rolodex(data)
    print r.run()
