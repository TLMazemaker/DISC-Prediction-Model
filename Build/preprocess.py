# Import libraries
import emoji
import re
import nlp_id

# Define a dictionary of common abbreviations and their expansions
abbreviations = {
    'sy': 'saya',
    'gw': 'gue',
    'km': 'kamu',
    'sgt': 'sangat',
    'yg': 'yang',
    'kgn': 'kangen',
    'dmn': 'dimana',
    'tdk': 'tidak',
    'tau': 'tahu',
    'jd': 'jadi',
    'gk': 'gak',
    'bgt': 'banget',
    'ak': 'aku',
    'ap': 'apa',
    'jgn':'jangan',
    'tu': 'itu',
    'mw': 'mau',
    'sm': 'sama',
    'lgsg': 'langsung',
    'boong': 'bohong',
    'yh': 'yah',
    'ygy': 'ya guys ya',
    'idk': 'saya tidak tahu',
    'brp': 'berapa',
    'byr': 'bayar',
    'mls': 'malas',
    'wtb': 'mau beli',
    'pvt': 'private',
    'bgtu': 'begitu',
    'ngga': 'nggak',
    'aj': 'aja',
    'gpp': 'tidak apa apa',
    'tbh': 'to be honest',
    'jg': 'juga',
    'tp': 'tapi',
    'u': 'kamu',
    'afh': 'apa',
    'iyh': 'iya',
    'tbtb': 'tiba tiba',
    'gws': 'semoga lekas sembuh',
    'dr': 'dari',
    'gf': 'pacar',
    'bf': 'pacar',
    'gurl': 'girl',
    'cpt': 'cepat',
    'sdh': 'sudah',
    'kt': 'kita',
    'sj': 'saja',
    'gt': 'gitu',
    'pls': 'please',
    'knp': 'kenapa',
    'kh': 'kah',
    'smgt': 'semangat',
    'lg': 'lagi',
    'wml': 'wish me luck',
    'blh': 'boleh',
    'td': 'tadi',
    'nd': 'tidak',
    'moga': 'semoga',
    'lngsng': 'langsung',
    'smoga': 'semoga',
    'bginian': 'beginian',
    'smoga': 'semoga',
    'thn': 'tahun',
    'dpn': 'depan',
    'pernahh': 'pernah',
    'blmpa': 'belum',
    'beluuum': 'belum',
    'blm': 'belum',
    'gmes': 'gemas',
    'smua': 'semua',
    'yaa': 'ya',
    'ajaa': 'aja',
    'tolonggg': 'tolong',
    'knpp': 'kenapa',
    'grindd': 'grind',
    'lessgo': "let's go",
    'ni': 'ini',
    'ovt': 'overthinking',
    'okeyy': 'okay',
    'apaaa': 'apa',
    'ajah': 'aja',
    'tuaa': 'tua',
    'adlh': 'adalah',
    'cb': 'coba',
    'ttp': 'tetap',
    'ham': 'hak asasi manusia',
    'jkw': 'jokowi',
    'timses': 'tim sukses',
    'w': 'gue',
    'omg': 'astaga',
    'bbrapa': 'beberapa',
    'bberapa': 'beberapa',
    'bbrp': 'beberapa',
    'tv': 'televisi',
    'capres': 'calon presiden',
    'cawapres': 'calon wakil presiden',
    'tsb': 'tersebut',
    'klo': 'kalau',
    'mnding': 'mending',
    'psing': 'pusing',
    'tgl': 'tanggal',
    'kmrin': 'kemarin',
    'kakel': 'kakak kelas',
    'mna': 'mana',
    'bljar': 'belajar',
    'skrg':'sekarang',
    'oengalaman': 'pengalaman',
    'org': 'orang',
    'eps': 'episode',
    'emg': 'memang',
    'kls': 'kelas',
    'sokab': 'sok akrab',
    'kyk': 'kayak',
    'orgil': 'orang gila',
    'bb': 'berat badan',
    'mkasih': 'terima kasih',
    'syg': 'sayang',
    'bleh': 'boleh',
    'sefang': 'sedang',
    'bs': 'bisa',
    'lelwat': 'lewat',
    'gmn': 'gimana',
    'fav': 'favorit',
    'tiba2': 'tiba-tiba',
    'ril': 'asli',
    'blg': 'bilang',
    'udh': 'udah',
    'bjngung': 'bingung',
    'mam': 'makan',
    'tf': 'transfer',
    'boleh2': 'boleh-boleh',
    'maba': 'mahasiswa baru',
    'jelel': 'jelek',
    'blom': 'belum',
    'blommm': 'belum',
    'sygku': 'sayangku',
    'syg': 'sayang',
    'trs': 'terus',
    'bnran': 'beneran',
    'bnr': 'benar',
    'ajg': 'anjing',
    'dh': 'sudah',
    'jdi': 'jadi',
    'twt': 'tweet',
    'mnis': 'manis',
    'ywdh': 'yaudah',
    'ajh': 'aja',
    'orang2': 'orang-orang',
    'org2': 'orang-orang',
    'nyindir2': 'nyindir-nyindir',
    'hrus': 'harus',
    'smpe': 'sampai',
    'msuk': 'masuk',
    'sbar': 'sabar',
    'cpat': 'cepat',
    'jdnya': 'jadinya',
    'psti': 'pasti',
    'smngt': 'semangat',
    'bngt': 'banget',
    'kl': 'kalau',
    'nnton': 'nonton',
    'hrs': 'harus',
    'tmen': 'teman',
    'masing2': 'masing-masing',
    'mksih': 'makasih',
    'pgn': 'ingin',
    'tpi': 'tapi',
    'msih': 'masih',
    'tbl': 'takut banget kamu',
    'dgn': 'dengan',
    'skalian': 'sekalian',
    'dgn': 'dengan',
    'utk': 'untuk',
    'byk': 'banyak',
    'bgtt': 'banget',
    'bgttt': 'banget',
    'aamiinn': 'amin',
    'skrgg': 'sekarang',
    'skrggg': 'sekarang',
    'bykk': 'banyak',
    'bykkk': 'banyak',
    'bykkkk': 'banyak',
    'bykkkkk': 'banyak',
    'cmn': 'cuman',
    'bnrn': 'beneran',
    'kmrn': 'kemarin',
    'utkmuuu': 'untuk mu',
    'bhs': 'bahasa',
    'krn': 'karena',
    'sklh': 'sekolah',
    'klw': 'kalau',
    'sblum': 'sebelum',
    'bsk': 'besok',
    'ortu': 'orang tua',
    'hbs': 'habis',
    'kpn': 'kapan',
    'slalu': 'selalu',
    'mentang2': 'mentang mentang',
    'dg': 'dengan',
    'dpt': 'dapat',
    'sayaaanggg': 'sayang',
    }

# Preprocess function
def normalize_tweet(tweet):

  # Normalize spaces and lowercase the text
  tweet = re.sub(r'\s+', ' ', tweet).strip().lower()

  # Replace numeric characters with their word equivalents
  for num, word in abbreviations.items():
      tweet = re.sub(r'\b' + num + r'\b', word, tweet)

  return tweet

def remove_emojis(tweet):
    # Regular expression to remove emojis
    tweet = emoji.replace_emoji(tweet, '')
    return tweet

def remove_links(tweet):
    # Regular expression to remove links
    return re.sub(r'http\S+', '', tweet)

def remove_mentions(tweet):
    # Regular expression to remove mentions
    return re.sub(r'@\w+', '', tweet)

def remove_hashtags(tweet):
    # Regular expression to remove hashtags
    return re.sub(r'#\w+', '', tweet)

def remove_special(tweet):
    # Define the pattern for special characters
    pattern = r'[^a-zA-Z0-9\s]'
    tweet = re.sub(pattern, '', tweet)

    return tweet

# Process tweets
def preprocess_tweet(tweet):
    tweet = remove_emojis(tweet)

    tweet = remove_links(tweet)

    tweet = remove_mentions(tweet)

    tweet = remove_hashtags(tweet)

    tweet = remove_special(tweet)

    tweet = normalize_tweet(tweet)

    return tweet

if 'dpt' in abbreviations:
    print('True')
else:
    print('False')
