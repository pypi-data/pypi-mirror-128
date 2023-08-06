
class Generator(object):

    # hostname = "Fun and Test Server";
    # motdInterval = 5;
    def simple_lineitem(self, key, value, quoted=False):
        if quoted:
            return f'{key} = "{value}";'
        else:
            return f'{key} = {value};'

    # missionWhitelist[] = {
    #   "direct_action_dev.Altis",
    # };
    # list_items('missionWhiteList', 'direct_action_dev.Altis', true, false)
    def list_items(self, key, values, quoted=False, newlines=True):

        product = []
        if newlines:
            newline = ""
        else:
            newline = "\n"
        if quoted:
            quote = '"'
        else:
            quote = ''

        product.append(f'{key}[] = {{{newline}')
        for item in values:
            product.append(f'  {quote}{item}{quote},{newline}')
        product.append(f'}};{newline}')

        return "".join(product)

    def generate(self):
        pass
