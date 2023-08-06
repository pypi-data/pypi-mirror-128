import base64
import random
import sys
from datetime import datetime
from threading import Event
from time import sleep


def compare_version(version: str, new_version: str):
    version_split = version.split('.')
    new_version_split = new_version.split('.')
    for index, sub_version in enumerate(version_split):
        if index >= len(new_version_split):
            return 'more'
        elif index + 1 == len(version_split) and index + 2 <= len(new_version_split):
            return 'less'
        elif int(sub_version) > int(new_version_split[index]):
            return 'more'
        elif int(sub_version) < int(new_version_split[index]):
            return 'less'
    return 'draw'


def validate_dict(dict_to_check: dict, example: (tuple, list), soft_check: bool = False):
    error_message = []
    for key in dict_to_check:
        if key not in example:
            error_message.append(f'Unavailable key "{key}". Must be one of {example.keys()}')
    if not soft_check:
        for key in example:
            if key not in dict_to_check:
                error_message.append(f'Missing requirements key "{key}". Requirements keys {dict_to_check.keys()}')
        if len(error_message) != 0:
            raise KeyError('\n'.join(error_message))
    else:
        if len(error_message) != 0:
            raise KeyError('\n'.join(error_message))
    return True


class Auth:
    def __init__(self, username, password):
        self.data = base64.b64encode(b':'.join((username.encode('ascii'),
                                                password.encode('ascii')))).strip().decode('ascii')

    def __call__(self, r):
        r.headers['Authorization'] = f'Basic {self.data}'
        return r

    def __del__(self):
        return 'BasicAuth'


class Host:
    def __init__(self, session, host):
        self.data = session.auth.data
        self.host = '' if host == '' else host.split('.', maxsplit=1)[1].replace('/', '')
        self.template = 'https://{}@ondemand.{}:443/wd/hub'

    def __str__(self):
        return self.template

    def __call__(self):
        return self.template.format(base64.b64decode(self.data).decode('utf-8'), self.host)


def print_progress(event: Event, progress_type: str):
    start, work, end = {
        'download': ('Start download file', 'Download time', 'Download finished'),
        'upload': ('Start upload file', 'Upload time', 'Upload finished'),
        'build': ('Start building file', 'Building time', 'Build finished')
    }.get(progress_type, ('Start', 'Time', 'End'))
    main_icon, meet = '🐱', ('🙈', '🙉', '🙊')
    enemy = ['🐲', '🐶', '🐭', '🐝', '🦄', '🐕', '🐳', '🦑', '🦂', '🐺', '🐼', '🐸']
    row = ['.' for _ in range(15)]
    row[1] = main_icon
    start_time = datetime.now()
    print(start)
    symbols, index = ('/', '|', '\\', '|'), 0
    while True:
        if row[1] != main_icon:
            row[1] = main_icon
        for position, value in enumerate(row):
            if value in enemy:
                if row[position - 1] == main_icon:
                    row[position - 1] = random.choice(meet)
                    row[position] = '.'
                else:
                    row[position - 1] = value
                    row[position] = '.'
        if random.randint(0, 6) == 3:
            row[-1] = random.choice(enemy)
        main_row = ''.join(row)
        txt = f'\r{work} {str(datetime.now() - start_time).split(".", maxsplit=1)[0]}...{symbols[index]}'
        sys.stdout.write(f'{txt} {main_row}')
        sys.stdout.flush()
        index += 1
        if index >= len(symbols):
            index = 0
        sleep(.3)
        if event.is_set():
            print(f'\n{end}', )
            break


def replace_html_tags(string_to_clear: str):
    html_tags = ['<!--...-->', '<!doctype>', '<a>', '<abbr>', '<acronym>', '<address>', '<applet>', '<area>',
                 '<article>', '<aside>', '<audio>', '<b>', '<base>', '<basefont>', '<bb>', '<bdo>', '<big>',
                 '<blockquote>', '<body>', '<br/>', '<button>', '<canvas>', '<caption>', '<center>', '<cite>',
                 '<code>', '<col>', '<colgroup>', '<command>', '<datagrid>', '<datalist>', '<dd>', '<del>',
                 '<details>', '<dfn>', '<dialog>', '<dir>', '<div>', '<dl>', '<dt>', '<em>', '<embed>',
                 '<eventsource>', '<fieldset>', '<figcaption>', '<figure>', '<font>', '<footer>', '<form>', '<frame>',
                 '<frameset>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<hgroup>',
                 '<hr/>', '<html>', '<i>', '<iframe>', '<img>', '<input>', '<ins>', '<isindex>', '<kbd>', '<keygen>',
                 '<label>', '<legend>', '<li>', '<link>', '<map>', '<mark>', '<menu>', '<meta>', '<meter>', '<nav>',
                 '<noframes>', '<noscript>', '<object>', '<ol>', '<optgroup>', '<option>', '<output>', '<p>',
                 '<param>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>', '<samp>', '<script>',
                 '<section>', '<select>', '<small>', '<source>', '<span>', '<strike>', '<strong>', '<style>', '<sub>',
                 '<sup>', '<table>', '<tbody>', '<td>', '<textarea>', '<tfoot>', '<th>', '<thead>', '<time>', '<title>',
                 '<tr>', '<track>', '<tt>', '<u>', '<ul>', '<var>', '<video>', '<wbr>', '</a>', '</abbr>', '</acronym>',
                 '</address>', '</applet>', '</area>', '</article>', '</aside>', '</audio>', '</b>', '</base>',
                 '</basefont>', '</bb>', '</bdo>', '</big>', '</blockquote>', '</body>', '</br/>', '</button>',
                 '</canvas>', '</caption>', '</center>', '</cite>', '</code>', '</col>', '</colgroup>', '</command>',
                 '</datagrid>', '</datalist>', '</dd>', '</del>', '</details>', '</dfn>', '</dialog>', '</dir>',
                 '</div>', '</dl>', '</dt>', '</em>', '</embed>', '</eventsource>', '</fieldset>', '</figcaption>',
                 '</figure>', '</font>', '</footer>', '</form>', '</frame>', '</frameset>',
                 '</h1>', '</h2>', '</h3>', '</h4>', '</h5>', '</h6>', '</head>', '</header>', '</hgroup>', '</hr/>',
                 '</html>', '</i>', '</iframe>', '</img>', '</input>', '</ins>', '</isindex>', '</kbd>', '</keygen>',
                 '</label>', '</legend>', '</li>', '</link>', '</map>', '</mark>', '</menu>', '</meta>', '</meter>',
                 '</nav>', '</noframes>', '</noscript>', '</object>', '</ol>', '</optgroup>', '</option>', '</output>',
                 '</p>', '</param>', '</pre>', '</progress>', '</q>', '</rp>', '</rt>', '</ruby>', '</s>', '</samp>',
                 '</script>', '</section>', '</select>', '</small>', '</source>', '</span>', '</strike>', '</strong>',
                 '</style>', '</sub>', '</sup>', '</table>', '</tbody>', '</td>', '</textarea>', '</tfoot>', '</th>',
                 '</thead>', '</time>', '</title>', '</tr>', '</track>', '</tt>', '</u>', '</ul>', '</var>', '</video>',
                 '</wbr>']
    for tag in html_tags:
        string_to_clear = string_to_clear.replace(tag, '')
    return string_to_clear


def get_dict_from_locals(locals_dict: dict, replace_underscore: bool = False):
    return {key.replace('from_', 'from').replace('_', '-') if replace_underscore else key: value for key, value in
            locals_dict.items() if key not in ('self', 'real_device') and '__py' not in key and value is not None}


def get_datetime_for_insights(start, end):
    if not isinstance(start, datetime):
        raise ValueError('Start time must be datetime')
    if not isinstance(start, datetime):
        raise ValueError('End time must be datetime')
    return start.strftime('%Y-%m-%dT%H:%M:%SZ'), end.strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_csv(csv_text: bytes):
    pass
