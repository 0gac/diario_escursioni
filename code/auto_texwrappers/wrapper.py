# data of interest
data = {
    "var_title": "Gita sul monte Terminillo",
    "var_date": "20/08/2024",
    "var_compagia": "Ceci e Michela Brands",
    "var_luogo_di_partenza": "Pian de valli",
    "var_start_ora": "9:20",
    "var_start_quota": "1650",
    "var_start_temperatura": "",
    "var_luogo_di_arrivo": "Pian de valli",
    "var_stop_ora": "17:00",
    "var_stop_quota": "1650",
    "var_stop_temperatura": "",
    "var_cimeraggiunte": "Terminilluccio, Terminillo",
    "var_kmtot": "10.35",
    "var_dislivello": "668",
    "var_durata": "5:48",
    "var_quotamax": "2210",
    "var_meteo": "C",
    "var_tipopercorso": "Anello",
    "var_difficolta": "E",
    "var_stanchezzaof5": "3",
    "var_esperienzaof5": "4",
    "path_copertina_img1": "../resources/cop1.png",
    "custompar_copertina_img1": ["", "", ""],
    "caption_copertina_img1": "Il sentiero che abbiamo trovato era più tecnico di quanto pensassi, il paesaggio era stupendo.",
    "path_copertina_img2": "../resources/cop2.png",
    "custompar_copertina_img2": ["", "", ""],
    "caption_copertina_img2": "Rifugio Rinaldi, visto dal sentiero preso per salire.",
    "var_pathgrafici": "../resources",    
    "path_grafpage_img1": "../resources/gra1.png",
    "custompar_grafpage_img1": ["", "", ""],
    "caption_grafpage_img1": "Rifugio Rinaldi.",
    "path_grafpage_img2": "../resources/gra2.png",
    "custompar_grafpage_img2": ["", "", ""],
    "caption_grafpage_img2": "Targa sulla cima del Terminillo.",
    "path_grafpage_img3": "../resources/gra3.png",
    "custompar_grafpage_img3": ["", "", ""],
    "caption_grafpage_img3": "alla fine del ripido sentiero per scendere da Terminillo, quasi a pranzo.",
    "var_NOTE": "Volevamo da tempo organizzare un trekking sugli appennini e finalmente siamo riusciti a trovare una giornata adatta. Purtroppo in grande parte delle zone attorno a noi faceva brutto tempo (monte vettore e massiccio del gran sasso), abbiamo quindi deciso di affrontare la salita sul monte Terminillo. \\Siamo partiti (io, Ceci e Michela) presto la mattina e quindi abbiamo iniziato a camminare poco dopo le 9, abbiamo anche fatto colazione in un baretto (Il bar di Heidi lol) vicino a dove abbiamo parcheggiato. Il posto era molto bello e la prima parte della salita molto semplice, seppur a tratti un pochettino ripida. La salita ci ha portati al rifugio Rinaldi, in compagnia di un gruppo di atletica giovanile di Roma (non proprio un'atmosfera pacifica e rilassante). Dopo un po' di riposo siamo ripartiti verso la cima, incontrando un sentiero più tecnico di quello che mi sarei aspettato ma comunque abbastanza breve. Purtroppo la vista dalla cima era oscurata dalle nuvole, ma comunque abbiamo trovato un bel paesaggio e un bel paio di personaggi piuttosto singolari (un po' merenderos ma neanche troppo, e un gruppo di vecchi rompipalle \"la montagna è di tutti ma...\"). Dopo una bella pausa in cima siamo scesi dall'altro lato della montagna alla volta del rifugio Sebastiani, la discesa è risultata piuttosto tecnica e ci abbiamo messo molto tempo (circa 2 ore). Arrivati al Sebastiani (che purtroppo era chiuso) abbiamo pranzato. \\Il ritorno è stato molto più semplice, 5 km circa in poco meno di un'ora, tutto pianeggiate attraverso un bel bosco. Tornati alla macchina abbiamo preso una fetta di torta nello stesso bar della colazione e dopo una breve pausa ci siamo avviati verso casa, passando per un negozio di scarpe a comprare le birkenstock tarocche per Ceci.",
    "path_fin_img1": "../resources/fin1.png",
    "custompar_fin_img1": ["", "", ""],
    "caption_fin_img1": "Le Brands in cima al Terminillo",
    "path_fin_img2": "../resources/fin2.png",
    "custompar_fin_img2": ["", "", ""],
    "caption_fin_img2": "",
    "path_fin_img3": "../resources/fin3.png",
    "custompar_fin_img3": ["", "0.5", "-90"],
    "caption_fin_img3": "il rifugio Rinaldi visto durante la discesa, nelle nuvole."
}

# -t 13:00 14:00 15:00 16:00 17:00 \
# lp upper right \

command_string_maps = "-p ../resources/track.gpx \
                       -op ../resources/ -t \
                       -mi 3 \
                       -v \
                       -bm"

# ================= execution ================= 
import json
import os
import imagesize

os.system("cd  ../resources; mogrify -format png *.jpg; mogrify -format png *.jpeg")
os.system("python ../src_mappe/analisys.py " + command_string_maps)

# latex wrapper 

def insertimage(imagepath, caption, cust_par, hasnumber = False):
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


data["var_copertina_img1"] = insertimage(data["path_copertina_img1"], data["caption_copertina_img1"], data["custompar_copertina_img1"])
data["var_copertina_img2"] = insertimage(data["path_copertina_img2"], data["caption_copertina_img2"], data["custompar_copertina_img2"])
data["var_grafpage_img1"] = insertimage(data["path_grafpage_img1"], data["caption_grafpage_img1"], data["custompar_grafpage_img1"], hasnumber = True)
data["var_grafpage_img2"] = insertimage(data["path_grafpage_img2"], data["caption_grafpage_img2"], data["custompar_grafpage_img2"], hasnumber = True)
data["var_grafpage_img3"] = insertimage(data["path_grafpage_img3"], data["caption_grafpage_img3"], data["custompar_grafpage_img3"], hasnumber = True)
data["var_fin_img1"] = insertimage(data["path_fin_img1"], data["caption_fin_img1"], data["custompar_fin_img1"])
data["var_fin_img2"] = insertimage(data["path_fin_img2"], data["caption_fin_img2"], data["custompar_fin_img2"])
data["var_fin_img3"] = insertimage(data["path_fin_img3"], data["caption_fin_img3"], data["custompar_fin_img3"])


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
    \\hspace*{{4cm}} Temperatura {var_start_temperatura}, \\\\
    \\\\
    \\faMapPin[regular] LUOGO DI ARRIVO: {var_luogo_di_arrivo},\\\\
    \\hspace*{{3.5cm}} Ora {var_stop_ora}, \\\\
    \\hspace*{{3.5cm}} Quota {var_stop_quota}, \\\\
    \\hspace*{{3.5cm}} Temperatura {var_stop_temperatura}, \\\\
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
\\begin{{minipage}}{{0.45\\linewidth}}
    \\centering
    {var_copertina_img1}
\\end{{minipage}}
\\begin{{minipage}}{{0.45\\linewidth}}
    \\centering
    {var_copertina_img2}
\\end{{minipage}}
\\end{{center}}

\\newpage

\\begin{{center}}

    % per mostrare i grafici fatti da src_mappe/analysis.py        
    \\begin{{minipage}}{{0.45\\linewidth}}
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

    \\vspace*{{1cm}}

    % foto relative alla mappa

    \\begin{{minipage}}{{0.3\\linewidth}}
        \\centering
        {var_grafpage_img1}
    \\end{{minipage}}
    \\begin{{minipage}}{{0.3\\linewidth}}
        \\centering
        {var_grafpage_img2}
    \\end{{minipage}}
    \\begin{{minipage}}{{0.3\\linewidth}}
        \\centering
        {var_grafpage_img3}
    \\end{{minipage}}
\\end{{center}}


\\newpage


\\begin{{center}}
    \\large{{NOTE: {var_NOTE} }}
\\end{{center}}



\\vspace*{{2cm}}

\\begin{{center}}
\\begin{{minipage}}{{0.45\\linewidth}}
    \\centering
    {var_fin_img1}
\\end{{minipage}}
\\begin{{minipage}}{{0.45\\linewidth}}
    \\centering
    {var_fin_img2}
\\end{{minipage}} 

\\vspace*{{.5cm}}
\\begin{{minipage}}{{0.45\\linewidth}}
    \\centering
    {var_fin_img3}
\\end{{minipage}}
\\end{{center}}



\\end{{document}}
""".format(**data)

# print((str))

with open("../src_tex/output.tex", "w") as f:
    f.write(str1)

os.system("pdflatex -interaction=batchmode -output-directory=../src_tex ../src_tex/output.tex")
os.system("evince ../src_tex/output.pdf")
