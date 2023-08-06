import os
from shutil import copy
from time import strftime
from ansi.colour.rgb import rgb8, rgb16, rgb256
from pyfiglet import Figlet
from ansi.colour import fg, bg, fx
from addict import Dict as Spezialdict
from box import Box
from itertools import product, cycle
from PIL import Image
from PIL import ImageEnhance


foreg = {
    "black": fg.black,
    "red": fg.red,
    "green": fg.green,
    "yellow": fg.yellow,
    "blue": fg.blue,
    "magenta": fg.magenta,
    "cyan": fg.cyan,
    "white": fg.white,
    "default": fg.default,
    "brightblack": fg.brightblack,
    "brightred": fg.brightred,
    "brightgreen": fg.brightgreen,
    "brightyellow": fg.brightyellow,
    "brightblue": fg.brightblue,
    "brightmagenta": fg.brightmagenta,
    "brightcyan": fg.brightcyan,
    "brightwhite": fg.brightwhite,
}

backg = {
    "black": bg.black,
    "red": bg.red,
    "green": bg.green,
    "yellow": bg.yellow,
    "blue": bg.blue,
    "magenta": bg.magenta,
    "cyan": bg.cyan,
    "white": bg.white,
    "default": bg.default,
    "brightblack": bg.brightblack,
    "brightred": bg.brightred,
    "brightgreen": bg.brightgreen,
    "brightyellow": bg.brightyellow,
    "brightblue": bg.brightblue,
    "brightmagenta": bg.brightmagenta,
    "brightcyan": bg.brightcyan,
    "brightwhite": bg.brightwhite,
}

# everythinh commented out is not working on my computer. Maybe you have more luck!!
effects = {
    "bold": fx.bold,
    #'faint'            :fx.faint,
    "italic": fx.italic,
    "underline": fx.underline,
    #'blink_slow'       :fx.blink_slow,
    #'blink'            :fx.blink,
    "negative": fx.negative,
    #'conceal'          :fx.conceal,
    "crossed_out": fx.crossed_out,
    #'font_reset'       :fx.font_reset,
    # 'font_1'           :fx.font_1,
    # 'font_2'           :fx.font_2,
    # 'font_3'           :fx.font_3,
    # 'font_4'           :fx.font_4,
    # 'font_5'           :fx.font_5,
    # 'font_6'           :fx.font_6,
    # 'font_7'           :fx.font_7,
    # 'font_8'           :fx.font_8,
    # 'font_9'           :fx.font_9,
    # 'fraktur'          :fx.fraktur,
    # 'gothic'           :fx.gothic,
    "underline_double": fx.underline_double,
    "normal": fx.normal,
    # 'not_italic'       :fx.not_italic,
    # 'not_fraktur'      :fx.not_fraktur,
    # 'not_gothic'       :fx.not_gothic,
    # 'not_underline'    :fx.not_underline,
    # 'steady'           :fx.steady,
    # 'positive'         :fx.positive,
    # 'reveal'           :fx.reveal,
    # 'overlined'        :fx.overlined,
    # 'not_framed'       :fx.not_framed,
    # 'not_encircled'    :fx.not_encircled,
    # 'not_overlined'    :fx.not_overlined
    "framed": fx.framed,
    "encircled": fx.encircled,
}


class Farbprinter:
    def __init__(self):
        self.p = self.create_printer()
        self.f = self.create_formater()
        self.figgi = Figlet()

    def _printer_erstellen(self, showall, create_printer, create_formater):
        pc_var = ""
        text = "text"
        p = Spezialdict()

        for indi, r in enumerate(product(list(foreg.keys()), list(backg.keys()))):
            if r[0] == r[1]:
                continue
            for schluessel, far in effects.items():
                if showall is True:
                    msg = (
                        far,
                        backg[r[0]],
                        foreg[r[1]],
                        f"""p.{r[1]}.{r[0]}.{schluessel}""",
                        far,
                        fx.reset,
                    )
                    print(f"""p.{r[1]}.{r[0]}.{schluessel}""".ljust(50), end=" -> ")
                    print("".join(map(str, msg)))
                if create_printer is True:
                    pc_var = f"""p.{r[1]}.{r[0]}.{schluessel} = lambda text: print(effects['{schluessel}'], backg['{r[1]}'], foreg['{r[0]}'], {text},effects['{schluessel}'],  fx.reset)"""
                if create_formater is True:
                    pc_var = f"""p.{r[1]}.{r[0]}.{schluessel} = lambda text: "".join(map(str,(effects['{schluessel}'], backg['{r[1]}'], foreg['{r[0]}'], {text},effects['{schluessel}'],  fx.reset)))"""
                if create_formater is True or create_printer is True:
                    exec(pc_var)
        if create_formater is True or create_printer is True:
            pc = Box(p.to_dict())
            return pc

    def p_show_all_color_combinations(self):
        self._printer_erstellen(
            showall=True, create_printer=False, create_formater=False
        )

    def create_printer(self):
        return self._printer_erstellen(
            showall=False, create_printer=True, create_formater=False
        )

    def create_formater(self):
        return self._printer_erstellen(
            showall=False, create_printer=False, create_formater=True
        )

    def save_file(self, path, content, overwrite=False):
        if overwrite is False:
            if os.path.exists(path):
                kleinerpfad = os.path.split(path)
                zeitstamp = strftime("backup_%Y_%m_%d_%H_%M_%S")
                kleinerpfad = list(kleinerpfad[:-1]) + [
                    zeitstamp + "_" + kleinerpfad[-1]
                ]
                ersterteil = kleinerpfad[0]
                for indexpf, einzelnepfade in enumerate(kleinerpfad):
                    if indexpf == 0:
                        continue
                    ersterteil = os.path.join(ersterteil, einzelnepfade)
                copy(path, ersterteil)
                print(f"File {path} already on HDD, backup created: {ersterteil}")
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)

    def _picture_to_bw(self, bild, threshhold):
        fn = lambda x: 255 if x > threshhold else 0
        bild = bild.convert("L").point(fn, mode="1")
        return bild.convert("RGB")

    def p_picture_to_ascii_art(
        self,
        picture_path,
        letter_for_ascii_art="PICTURE",
        contrast=1,
        desired_width=80,
        savetopath=None,
        printpicture=False,
        black_and_white=False,
        black_and_white_thresh=50,
        rgb8_16_256=8,
    ):
        bild = Image.open(picture_path)
        if black_and_white is True:
            bild = self._picture_to_bw(bild, black_and_white_thresh)
        altebreite, altehoehe = bild.size
        neuebreite = desired_width
        faktor = altebreite / neuebreite
        neuehoehe = int(altehoehe / faktor)
        bild = bild.resize((int(neuebreite * 2.66), neuehoehe))
        enh = ImageEnhance.Contrast(bild)
        bild = enh.enhance(contrast)
        bild = bild.getdata()
        groesse_x = bild.size[0]
        bild = list(bild)
        asciibildfarbe = []
        for indexpixel_pixxel, setwiederholen in zip(
            enumerate(bild), cycle(letter_for_ascii_art)
        ):
            indexpixel, pixxel = indexpixel_pixxel
            if rgb8_16_256 == 8:
                asciibildfarbe.append(
                    "".join(
                        map(
                            str,
                            (
                                fx.bold,
                                bg.black,
                                rgb8(pixxel[0], pixxel[1], pixxel[2]),
                                setwiederholen,
                                bg.black,
                                fx.bold,
                                fx.reset,
                            ),
                        )
                    )
                )
            if rgb8_16_256 == 16:
                asciibildfarbe.append(
                    "".join(
                        map(
                            str,
                            (
                                fx.bold,
                                bg.black,
                                rgb16(pixxel[0], pixxel[1], pixxel[2]),
                                setwiederholen,
                                bg.black,
                                fx.bold,
                                fx.reset,
                            ),
                        )
                    )
                )
            if rgb8_16_256 == 256:
                asciibildfarbe.append(
                    "".join(
                        map(
                            str,
                            (
                                fx.bold,
                                bg.black,
                                rgb256(pixxel[0], pixxel[1], pixxel[2]),
                                setwiederholen,
                                bg.black,
                                fx.bold,
                                fx.reset,
                            ),
                        )
                    )
                )
            if (indexpixel + 1) % groesse_x == 0:
                asciibildfarbe.append("\033[0m\n")
        fertigesbild = "".join(map(str, asciibildfarbe)) + "\n"
        if savetopath is not None:
            self.save_file(savetopath, fertigesbild)
        if printpicture is True:
            print(fertigesbild)
        return fertigesbild

    @staticmethod
    def p_pandas_list_dict(
        list_df_series_dict, linebreak=50, header=None, listtranspose=False
    ):
        tabelle = list_df_series_dict.copy()
        tabelleformatiert = []

        def farbe_auswaehlen(farbindex, wort, rechtsfuellen, linksfuellen):
            wort = f"{wort}"
            farben = {
                0: (
                    "black_red",
                    f"\033[1;31;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                1: (
                    "black_green",
                    f"\033[1;32;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                2: (
                    "black_yellow",
                    f"\033[1;33;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                3: (
                    "black_blue",
                    f"\033[1;34;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                4: (
                    "black_purple",
                    f"\033[1;35;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                5: (
                    "black_cyan",
                    f"\033[1;36;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
                6: (
                    "black_grey",
                    f"\033[1;37;40m{wort.rjust(rechtsfuellen).ljust(linksfuellen)}\033[1;33;40m▓\033[0m",
                ),
            }
            return farben[farbindex][1]

        def maximallaenge_von_listen_holen(listexxx):
            tliste = [list(xaaa) for xaaa in zip(*listexxx)]
            tliste = [max([len(xx) for xx in yy]) for yy in tliste]
            return tliste

        def listen_auf_gleiche_laenge_bringen(liste):
            listezumverlaengern = liste.copy()
            langevonjederliste = [len(xx) for xx in listezumverlaengern]
            maxlaengegroessteliste = max(langevonjederliste)
            try:
                listezumverlaengern = [
                    xx + [" "] * (maxlaengegroessteliste - len(xx))
                    for xx in listezumverlaengern
                ]
            except:
                pass
            return listezumverlaengern

        if isinstance(tabelle, dict):
            if header is not None:
                if len(header) != 2:
                    header = ["keys", "items"]

            tabelle = [list(v) for v in tabelle.items()]

        if isinstance(tabelle, list):
            try:
                tabelle = listen_auf_gleiche_laenge_bringen(liste=tabelle)
            except:
                try:
                    tabelle = [[tab] for tab in tabelle]
                    tabelle = listen_auf_gleiche_laenge_bringen(liste=tabelle)
                except:
                    pass
                pass
            try:
                for tab in tabelle:
                    if isinstance(tab, list):
                        tabelleformatiert = [
                            [str(xx) for xx in text] for text in tabelle
                        ]
                        break
            except:
                tabelleformatiert = [[str(text)[:linebreak]] for text in tabelle]
            if not any(tabelleformatiert):
                tabelleformatiert = [[str(text)[:linebreak]] for text in tabelle]
            if listtranspose is True:
                tabelleformatiert = [list(xaaa) for xaaa in zip(*tabelleformatiert)]
        if "DataFrame" in str(type(tabelle)) or "Series" in str(type(tabelle)):
            if "Series" in str(type(tabelle)):
                df2 = tabelle.to_frame().copy()
            if "DataFrame" in str(type(tabelle)):
                df2 = tabelle.copy()
            df2.insert(loc=0, column="INDEX", value=df2.index.to_list())
            for col in df2.columns:
                df2[col] = df2[col].apply(lambda x: str(x)[:linebreak])
            for rownummer in range(df2.shape[0]):
                tabellex = [str(text) for text in df2.iloc[rownummer]]

                tabelleformatiert.append(tabellex.copy())
            header = df2.columns.to_list()
        maximallaengen = maximallaenge_von_listen_holen(tabelleformatiert)
        if header is not None:
            headermitmaximalvergleichen = []
            headermaximal = [len(str(xx)) for xx in header]
            for h, m in zip(headermaximal, maximallaengen):

                if h > m:
                    headermitmaximalvergleichen.append(h)
                    continue
                headermitmaximalvergleichen.append(m)
            maximallaengen = headermitmaximalvergleichen.copy()

        if header is not None:
            maxlen = list(zip(header, maximallaengen))
            for header_text, maximalausfuellen in maxlen:
                rechtsfuellen_h = 1
                linksfuellen_h = maximalausfuellen
                header_text = (
                    str("" + str(header_text))
                    .rjust(rechtsfuellen_h)
                    .ljust(linksfuellen_h)
                )
                print(f"\033[43;1m\033[30m  {header_text}  \033[30m▓\033[0m", end="")
            print(" ")
        for eintrag in tabelleformatiert:
            durchzaehlen = 0
            for satz, colourloop in zip(eintrag, cycle(range(7))):
                satz = " " * (maximallaengen[durchzaehlen] - len(satz)) + satz
                wasdrucken = farbe_auswaehlen(
                    farbindex=colourloop,
                    wort=f"  {satz}  ",
                    rechtsfuellen=1,
                    linksfuellen=maximallaengen[durchzaehlen],
                )
                print(wasdrucken, end="")
                durchzaehlen = durchzaehlen + 1
            print(" ")
        print("\033[0m")

    def farbe_auswaehlen(
        self, wort, colorfunction, rechtsfuellen, linksfuellen, offsetanfang=0
    ):
        wort = f"{wort}"
        rechtsfuellen = rechtsfuellen * " "
        offsetanfang = offsetanfang * " "
        print(offsetanfang, end="")
        return colorfunction(f"""{rechtsfuellen}{wort.ljust(linksfuellen)}""")

    def p_ascii_font_2_colors(
        self,
        text,
        colorfunction=None,
        font=None,
        width=1000,
        offset_from_left_side=25,
        offset_from_text=5,
    ):
        offset_without_color_left = offset_from_left_side
        offset_right_left_colored_part = offset_from_text
        allfonts = [font]
        if colorfunction is None:
            print(
                "You have not choosen a color function! Use for example: colorfunction=drucker.f.black.green.italic ! I will print the text using this color to show you how it looks like!!"
            )
            colorfunction = self.f.black.green.italic
        if font is None:
            print("Font is None, I will show you all fonts that I have! :)")
            allfonts = self.figgi.getFonts()
        for schrift in allfonts:
            f = Figlet(font=schrift, width=width)
            textschreiben = f.renderText(text)
            geteiltertext = textschreiben.splitlines()
            laengstertext = [len(te) for te in geteiltertext]
            laengstertext.sort()
            laengstertext = laengstertext[-1]

            if font is None:
                print(f"Name of the next font: {schrift}")
            for num, zeile in enumerate(textschreiben.splitlines()):
                if font is None:
                    print(str(num).zfill(5), end="")
                print(
                    self.farbe_auswaehlen(
                        wort=zeile,
                        colorfunction=colorfunction,
                        rechtsfuellen=offset_right_left_colored_part,
                        linksfuellen=laengstertext + offset_right_left_colored_part,
                        offsetanfang=offset_without_color_left,
                    )
                )

    def print_flag(
        self, worter, colorfunctions, rechtsfuellen, linksfuellen, offsetanfang=0
    ):
        n, p = len(worter), len(colorfunctions)
        c, r = divmod(n, p)
        ganzelistemultiplizieren = [c] * (p - r) + [c + 1] * r
        ganzelistemultiplizieren.sort(reverse=True)
        colorlistealle = []
        for indexcolor, subliste in enumerate(ganzelistemultiplizieren):
            for nummerieren in range(subliste):
                colorlistealle.append(colorfunctions[indexcolor])
        rechtsfuellen_string = rechtsfuellen * " "
        offsetanfang_string = offsetanfang * "\033[0m" + " " + "\033[0m"
        woerterzusammen = []
        for wort, farbed in zip(worter, colorlistealle):
            wort = f"{wort}"
            formatierterstring = f"""{rechtsfuellen_string}{wort.ljust(linksfuellen)}"""
            formatierterstring = farbed(formatierterstring)
            woerterzusammen.append(offsetanfang_string + formatierterstring)
        return woerterzusammen

    def p_ascii_font_on_flag(
        self,
        text,
        colorfunctions=None,
        font=None,
        width=1000,
        offset_from_left_side=25,
        offset_from_text=5,
    ):
        offset_without_color_left = offset_from_left_side
        offset_right_left_colored_part = offset_from_text
        allfonts = [font]

        if not any(colorfunctions):
            print(
                "You haven't choosen any colorfunctions! Use (e.g.) colorfunctions= [drucker.f.black.brightyellow.normal, drucker.f.brightred.black.normal, drucker.f.brightyellow.black.normal] ! I will print the text using this colors to show you how it looks like!"
            )
            colorfunctions = [
                self.f.black.brightyellow.normal,
                self.f.brightred.black.normal,
                self.f.brightyellow.black.normal,
            ]
        if font is None:
            print("Font is None, I will show you all fonts that I have! :)")
            allfonts = self.figgi.getFonts()
        for schrift in allfonts:
            f = Figlet(font=schrift, width=width)
            textschreiben = f.renderText(text)
            geteiltertext = textschreiben.splitlines()
            laengstertext = [len(te) for te in geteiltertext]
            laengstertext.sort()
            laengstertext = laengstertext[-1]

            if font is None:
                print(f"Name of the next font: {schrift}")
            formatiert = self.print_flag(
                worter=geteiltertext,
                colorfunctions=colorfunctions,
                rechtsfuellen=offset_right_left_colored_part,
                linksfuellen=laengstertext + offset_right_left_colored_part,
                offsetanfang=offset_without_color_left,
            )
            for textformatiert in formatiert:
                print(offset_without_color_left * " ", end="")
                print(textformatiert)

    def print_flag_with_border(
        self,
        worter,
        colorfunctions,
        bordercolorfunction,
        rechtsfuellen,
        linksfuellen,
        offsetanfang=0,
    ):
        n, p = len(worter), len(colorfunctions)
        c, r = divmod(n, p)
        ganzelistemultiplizieren = [c] * (p - r) + [c + 1] * r
        ganzelistemultiplizieren.sort(reverse=True)
        colorlistealle = []
        for indexcolor, subliste in enumerate(ganzelistemultiplizieren):
            for nummerieren in range(subliste):
                colorlistealle.append(colorfunctions[indexcolor])
        rechtsfuellen_string = rechtsfuellen * " "
        offsetanfang_string = offsetanfang * "\033[0m" + " " + "\033[0m"
        woerterzusammen = []
        string_border = (
            offsetanfang_string
            + bordercolorfunction("▓" * (linksfuellen + rechtsfuellen + 2))
            + offsetanfang_string
        )
        woerterzusammen.append(string_border)
        for wort, farbed in zip(worter, colorlistealle):
            wort = f"{wort}"
            formatierterstring = f"""{rechtsfuellen_string}{wort.ljust(linksfuellen)}"""
            formatierterstring = (
                bordercolorfunction("▓")
                + farbed(formatierterstring)
                + bordercolorfunction("▓")
            )
            woerterzusammen.append(offsetanfang_string + formatierterstring)
        woerterzusammen.append(string_border)
        woerterzusammen.append("\033[0m")
        return woerterzusammen

    def p_ascii_front_on_flag_with_border(
        self,
        text,
        colorfunctions=None,
        bordercolorfunction=None,
        font=None,
        width=1000,
        offset_from_left_side=25,
        offset_from_text=5,
    ):
        offset_without_color_left = offset_from_left_side
        offset_right_left_colored_part = offset_from_text
        allfonts = [font]

        if not any(colorfunctions):
            print(
                "You haven't choosen any colorfunctions! Use (e.g.) colorfunctions= [drucker.f.black.brightyellow.normal, drucker.f.brightred.black.normal, drucker.f.brightyellow.black.normal]  bordercolorfunction = drucker.f.yellow.green.bold ! I will print the text using this colors to show you how it looks like!"
            )
            colorfunctions = [
                self.f.black.brightyellow.normal,
                self.f.brightred.black.normal,
                self.f.brightyellow.black.normal,
            ]
            bordercolorfunction = self.f.yellow.green.bold
        if font is None:
            print("Font is None, I will show you all fonts that I have! :)")
            allfonts = self.figgi.getFonts()
        for schrift in allfonts:
            f = Figlet(font=schrift, width=width)
            textschreiben = f.renderText(text)
            geteiltertext = textschreiben.splitlines()
            laengstertext = [len(te) for te in geteiltertext]
            laengstertext.sort()
            laengstertext = laengstertext[-1]

            if font is None:
                print(f"Name of the next font: {schrift}")
            formatiert = self.print_flag_with_border(
                worter=geteiltertext,
                colorfunctions=colorfunctions,
                bordercolorfunction=bordercolorfunction,
                rechtsfuellen=offset_right_left_colored_part,
                linksfuellen=laengstertext + offset_right_left_colored_part,
                offsetanfang=offset_without_color_left,
            )
            for textformatiert in formatiert:
                print(offset_without_color_left * " ", end="")
                print(textformatiert)
