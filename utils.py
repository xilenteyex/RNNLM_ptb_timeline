import json

def read_json_file(fname):
        with open(fname, 'r') as f:
                # data = f.read()
                # print(data[176257])
                # to_print = data[176200:176259]
                # for ch in to_print:
                #       print("ch : ", ch)
                #       print("asci : ", ord(ch))
                # print("*****")
                # data.replace('\x02', '')
                # data.replace('\x19', '')
                # m = json.loads(data)
                m = json.load(f)

                # m = str(m)
                # print("type of m ::::::::::::::::::::::::")
                # print(type(m))

        ## Sometimes u get str instead of dict (dunno why) ##
        if not isinstance(m, dict) and not isinstance(m, list):
                m = str(m)
                return json.loads(m)
        return m

