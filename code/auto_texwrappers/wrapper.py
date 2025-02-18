# data of interest
nota = """
Da trento sono passati a prendermi attorno alle 8 a egna. Con oslo alla guida siamo arrivati a pfelders attorno alle 9.30 insieme agli altri.

Dopo aver parcheggiato e sistemato l'attrezzatura per la partenza alcuni si sono fermati a prendere un caffe/gelato, facendo subito chiaro l' andazzo dei prossimi giorni. In ogni caso siamo partiti attorno alle 10.

Fin dall'inizio della giornata era chiaro che ci saremmo separati per poi ritrovarci al rifugio. Così dopo un po io, Oslo, Zen, Dani siamo rimasti da soli davanti tenendo un ottimo ritmo che ci ha consentito di raggiungere il rifugio attorno alle 13.30 (per quanto riguarda me e Daniele. Oslo e Zen sono andati un po avanti e sono arrivati 15/20 minuti prima di noi). La salita è costantemente ripida e piuttosto faticosa ma l'ho affrontata facendo poche pause e salendo ad un ritmo coatante, probabilmente troppo veloce e questo mi darà problemi a dormire (non io che scrivo sta roba la notte invece che dormire). Durante la salita ho potuto usare il nuovo filtro, rivelatosi un ottimo acquisto.

Le successive ore le ho passate all'insegna del relax, mentre i miei tre compagni di avventure andavano ad esplorare la cima altissima io ho aspettato gli altri, bevuto un radler e preso una fetta di torta. Una volta arrivati e riposati tutti, io, Mary, Paolo e Taba abbiamo seguito le indicazioni del rifugista per provare a raggiungere una cima un po piu bassa vicino al rifugio (sarebbe stata la mia prima 3000), purtroppo il sentiero era troppo brutto e siamo dovuti scendere prima della cima.

Un po sconfitti siamo tornati in rifugio, io e Paolo abbiamo fatto un po di ricognizione per trovare un posto adatto a piantare le tende e poco dopo ci siamo avviati verso la cena. La cena è stata ottima (gulash suppe), il rifugio è bellissimo e sarebbe bello tornarci anche per provare a dormirci. Anche la zona è bellissima, completamente diverso dal trentino ma veramente un posto suggestivo (dal rifugio e dalla tenda si sentivwno gli echi delle valanghe nei ghiacciai austriaci 

Dopo cena abbiamo fatto un momento socialità prima di dirigerci a montare le tende (psr la prima volta ho montato la tenda nuova ed è stato davvero un piacere). Una volta montate Oslo è tornato al rifugio a fare chiacchiere metre io e Paolo siamo rimasti a chiacchierare un po con Zen e Andrei che sono venuti a trovarci. Salutati Zen e Andrei ci siamo messi a letto (prestissimo, attorno alle 21) perché domani ci aspetta una sveglia alle 3.30 :(.
"""
enable_image_conversion = False
enable_graf_generation = False
print_result = False
data = {
    "var_title": "Giro pazzo Tessa - Primo giorno",
    "var_date": "05/08/2024",
    "var_compagia": "Brosdi",
    "var_luogo_di_partenza": "Moso in passiria",
    "var_start_ora": "9:50",
    "var_start_quota": "1630",
    "var_start_temperatura": "",
    "var_luogo_di_arrivo": "Rifugio Petrarca",
    "var_stop_ora": "13:20",
    "var_stop_quota": "2870",
    "var_stop_temperatura": "",
    "var_cimeraggiunte": "\\faTimesCircle",
    "var_kmtot": "10.21",
    "var_dislivello": "1250",
    "var_durata": "3:30",
    "var_quotamax": "2870",
    "var_meteo": "C",
    "var_tipopercorso": "A", # A, AR, Anello
    "var_difficolta": "E", # T, E, EE, EEA
    "var_stanchezzaof5": "5",
    "var_esperienzaof5": "5",
    "images_copertina": [
        ["../resources/hohewilde.png", ("1", "", ""), "Cima Hohewilde, la saliremo domani mattina, Oslo, Zen e Dani la saliranno nel pomeriggio."], # path, (heigth, width, angle), caption    
        ["../resources/valle_inizio.png", ("1", "", ""), "La stupenda valle che abbiamo risalito per raggiungere il Rifugio Petrarca."]  # path, (heigth, width, angle), caption    
    ],
    "var_pathgrafici": "../resources",    
    "images_grafpage": [
        ["../resources/valle_inizio_dall_alto.png", ("1", "", ""), "La valle che abbiamo risalito, vista dall'alto."], # path, (heigth, width, angle), caption    
        ["../resources/vista_da_petrarca.png", ("1", "", ""), "Vista sul laghetto e sulle cime dal rifugio Petrarca."], # path, (heigth, width, angle), caption    
        ["../resources/petrarca_da_gelato.png", ("1", "", ""), "Vista dell'appena ristrutturato rifugio da Passo Gelato."]  # path, (heigth, width, angle), caption    
    ],
    "var_NOTE": nota,
    "images_fin": [
        ["../resources/saludo.png", (".65", "", ""), "Vista da passo Gelato del nostro campo per la notte."], # path, (heigth, width, angle), caption    
        ["../resources/paeolo_snacc.png", (".65", "", ""), "Paolo esce il limoncello, inizia la festa al campo del sesso."], # path, (heigth, width, angle), caption    
        ["../resources/oslo_cima.png", (".65", "", ""), "Oslo, Zen e Dani, pazzi matti sgravati scalano Hohewilde il pomeriggio del primo giorno (e Dani e Oslo, pazzissimi, mattissimi e sgravatissimi anche la mattina dopo)."]  # path, (heigth, width, angle), caption    
    ]
}

# -t 13:00 14:00 15:00 16:00 17:00 \
# lp upper right \

command_string_maps = f"-p ../resources/track.gpx \
                       -op ../resources/ -t \
                       -mi {len(data["images_grafpage"])} \
                       -v \
                       -bm \
                       -lp lower right"

# ================= execution ================= 
import json
import os
import imagesize

if enable_image_conversion:
    os.system("cd  ../resources; mogrify -format png *.jpg; mogrify -format png *.jpeg")

if enable_graf_generation:
    os.system("python ../src_mappe/analisys.py " + command_string_maps)

# images

def imgstr(imagepath, cust_par, caption, hasnumber = False):
    w, h = imagesize.get(imagepath)
    strdim = ""
    if cust_par[0] != "":
        width = cust_par[0]
        strdim += "width = " + width + "\\linewidth"
    if cust_par[1] != "":
        height = cust_par[1]
        if strdim != "":
            strdim += ", "
        strdim += "height = " + height + "\\linewidth"
    if strdim == "":
        if w > h:
            strdim = "width = 0.8\\linewidth"
        if h > w:
            strdim = "height = 0.8\\linewidth"
    if cust_par[2] != "":
        angle = cust_par[2]
        strdim += ", angle = " + angle

    str1 = "\\captionsetup{{width = 0.8 \\linewidth}}\n"
    str2 = "\\includegraphics["+strdim+"]{{\"{var_imagepath}\"}}\n".format(var_imagepath = imagepath)
    if hasnumber:
        str3 = "\\captionof{{figure}}{{{var_caption}}}\n".format(var_caption = caption)
    else:
        str3 = "\\captionof*{{figure}}{{{var_caption}}}\n".format(var_caption = caption)
    str = str1 + str2 + str3
    return str

def gentab(images, compact = False):
    str_minipage = """\\begin{{minipage}}{{ {width} \\linewidth}}\n\\centering\n{img}\\end{{minipage}}\n"""
    
    str = ""
    if len(images) == 2:
        str = str_minipage.format(width = "0.45", img = images[0][3]) \
            + str_minipage.format(width = "0.45", img = images[1][3])
    if len(images) == 3:
        if compact:
            str = str_minipage.format(width = "0.3", img = images[0][3]) \
                + str_minipage.format(width = "0.3", img = images[1][3]) \
                + str_minipage.format(width = "0.3", img = images[2][3])
        else: 
            str = str_minipage.format(width = "0.45", img = images[0][3]) \
                + str_minipage.format(width = "0.45", img = images[1][3]) \
                + "\n\n" \
                + str_minipage.format(width = "0.45", img = images[2][3])
    if len(images) == 4:
        str = str_minipage.format(width = "0.45", img = images[0][3]) \
            + str_minipage.format(width = "0.45", img = images[1][3]) \
            + "\n\n" \
            + str_minipage.format(width = "0.45", img = images[2][3]) \
            + str_minipage.format(width = "0.45", img = images[3][3]) 
    return str

for image in data["images_copertina"]:
    image.append(imgstr(*image))
data["var_img_copertina"] = gentab(data["images_copertina"])

for image in data["images_grafpage"]:
    image.append(imgstr(*image, hasnumber=True))
data["var_img_grafpage"] = gentab(data["images_grafpage"], compact = True) 

for image in data["images_fin"]:
    image.append(imgstr(*image))
data["var_img_fin"] = gentab(data["images_fin"])

# temperature 

if data["var_start_temperatura"] != "":
    temp = data["var_start_temperatura"]
    data["var_start_temperatura"] = f"\\hspace*{{4cm}} Temperatura {temp}, \\\\"

if data["var_stop_temperatura"] != "":
    temp = data["var_stop_temperatura"]
    data["var_stop_temperatura"] = f"\\hspace*{{3.5cm}} Temperatura {temp}, \\\\"

# Grafici 

hashr = os.path.exists(data["var_pathgrafici"] + "/hr.png")
hasele = os.path.exists(data["var_pathgrafici"] + "/ele.png")
if hashr and hasele: 
    data["var_grafici"] = """\\begin{{minipage}}{{0.45\\linewidth}}
        \\centering
        \\faMountain \\quad \\large{{Altitudine}}\\\\
        \\includegraphics[scale = 0.5]{{"{var_pathgrafici}/ele.png"}}
    \\end{{minipage}}
    \\begin{{minipage}}{{0.45\\linewidth}}
        \\centering
        \\faHeartbeat \\quad \\large{{Frequenza cardiaca}}\\\\
        \\includegraphics[scale = 0.5]{{"{var_pathgrafici}/hr.png"}}
    \\end{{minipage}} \\\\
    \\begin{{minipage}}{{\\linewidth}}
        \\vspace*{{0.5cm}}
        \\centering
        \\faMapSigns \\quad \\large{{Traccia GPS}}\\\\
        \\includegraphics[scale = 0.60]{{"{var_pathgrafici}/track.png"}}
    \\end{{minipage}}
    \\vspace*{{1cm}}""".format(**data)

if hasele and not hashr: 
    data["var_grafici"] = """\\begin{{minipage}}{{0.5\\linewidth}}
        \\centering
        \\faMountain \\quad \\large{{Altitudine}}\\\\
        \\includegraphics[scale = 0.5]{{"{var_pathgrafici}/ele.png"}}
    \\end{{minipage}}

    \\begin{{minipage}}{{\\linewidth}}
        \\vspace*{{0.5cm}}
        \\centering
        \\faMapSigns \\quad \\large{{Traccia GPS}}\\\\
        \\includegraphics[scale = 0.60]{{"{var_pathgrafici}/track.png"}}
    \\end{{minipage}}
    \\vspace*{{1cm}}""".format(**data)


# TeX

str1 = """
\\documentclass{{article}}
\\usepackage{{common/pacchetti}}
\\title{{\\Huge Escursione: {var_title} }}
\\date{{}}
\\author{{}}
\\begin{{document}}
\\input{{common/valutazione.tex}}
\\input{{common/difficolta.tex}}
\\input{{common/meteo.tex}}
\\input{{common/tipo_percorso.tex}}
\\maketitle
\\begin{{minipage}}[t]{{0.5\\textwidth}}
    \\faCalendar* DATA: {var_date}\\\\
    \\\\
    \\faSmile[regular] COMPAGNIA: {var_compagia}\\\\
    \\\\
    \\faMapPin[regular] LUOGO DI PARTENZA: {var_luogo_di_partenza}, \\\\
    \\hspace*{{4cm}} Ora {var_start_ora}, \\\\
    \\hspace*{{4cm}} Quota {var_start_quota}, \\\\
    {var_start_temperatura} 
    \\\\
    \\faMapPin[regular] LUOGO DI ARRIVO: {var_luogo_di_arrivo},\\\\
    \\hspace*{{3.5cm}} Ora {var_stop_ora}, \\\\
    \\hspace*{{3.5cm}} Quota {var_stop_quota}, \\\\
    {var_stop_temperatura}
    \\\\
    \\faMountain[regular] CIME RAGGIUNTE: {var_cimeraggiunte}\\\\
    %\\\\
    \\vspace*{{1cm}}\\\\
    KM PERCORSI:{var_kmtot} \\\\
    DISLIVELLO: {var_dislivello}\\\\
    DURATA: {var_durata}\\\\
    QUOTA MASSIMA: {var_quotamax}\\\\
\\end{{minipage}} 
%NON INIZIARE NUOVO PARAGRAFO
\\begin{{minipage}}[t]{{0.4\\textwidth}}
    METEO: \\\\ \\\\
    \\meteo{{{var_meteo}}}
    TIPO DI PERCORSO: \\\\ \\\\
    \\tipopercorso{{{var_tipopercorso}}}
    LIVELLO DI DIFFICOLT\\'A: \\\\ \\\\
    \\difficolta{{{var_difficolta}}}
\\end{{minipage}}
\\begin{{center}}
    \\raisebox{{-7ex}}{{
        \\begin{{minipage}}[H]{{0.5\\textwidth}} %non riesco a togliere gli errori qui :(
            \\stanchezza{{{var_stanchezzaof5}}}{{5}}\\\\ %es: livello di stanchezza 2 su 5
            \\\\
            \\esperienza{{{var_esperienzaof5}}}{{5}}  %es: valutazione generale 3 su 5
        \\end{{minipage}}
    }}
\\vspace*{{1cm}}

% tabella con due foto, tipo copertina
{var_img_copertina}

\\newpage
\\begin{{center}}

    {var_grafici}

    % foto relative alla mappa
    {var_img_grafpage}

\\end{{center}}
\\newpage
\\begin{{center}}
    \\large{{NOTE: {var_NOTE} }}
\\end{{center}}
\\vspace*{{2cm}}
\\begin{{center}}

{var_img_fin}

\\end{{center}}
\\end{{document}}
""".format(**data)

if print_result: 
    print((str))

if not print_result:
    with open("../src_tex/output.tex", "w") as f:
        f.write(str1)

    os.system("pdflatex -interaction=batchmode -output-directory=../src_tex ../src_tex/output.tex")
    os.system("evince ../src_tex/output.pdf")
