
# Helper function making reading external override easier
def parse_value_override(arg):
    i = arg.index("=")
    key = arg[:i].strip()
    val = arg[i+1:].strip()
    return {key:val}


def format_flyway(input_data):
    
    def r_formatter(d, leading=""):
        formatted = []
        for key,value in d.items():

            full_key = ".".join([x for x in [leading, key] if x.strip() != ""])
            if value.__class__ == dict:
                formatted += r_formatter(value, full_key)
            else:
                p = "{} = {}".format(full_key, value )
                formatted.append(p)
        return formatted

    return "\n".join(r_formatter(input_data))



