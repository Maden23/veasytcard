from selenium import webdriver
from PIL import Image, ImageDraw, ImageFont
import copy
import math
import random
import pathlib

path = pathlib.Path(__file__).parent.absolute()


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def runAlg(mainText, tagline, siteAddress, phone, mail, logoPath, finalPath):

    width, height = 900, 250
    options = webdriver.ChromeOptions()
    '''options.add_argument('headless')'''
    options.add_argument(f'window-size={width},{height}')

    driver = webdriver.Chrome(chrome_options = options)
    #  https://burgerking.ru
    #  http://nadin.miem.edu.ru
    #  https://auto.ru
    driver.get(siteAddress) 
    elements = driver.find_elements_by_tag_name('body')
    el_num = 0
    for el in elements:
        elements[el_num].screenshot("screenshot" + str(el_num) + ".png")
        el_num += 1
    driver.quit()

    '''-------------------------------------------------------------------------Вычисление цветов'''
    color = list()
    colorsNum = list()
    for scr in range(el_num):
        img = Image.open("screenshot" + str(scr) + ".png")
        obj = img.load()
        (width, height) = img.size

        width_m = 50
        height_m = 50

        if height != height_m:
            rows = (height // height_m) + 1
        else:
            rows = 1

        if width != width_m:
            cols = (width // width_m) + 1
        else:
            cols = 1

        if height > height_m:
            fin_row = height % height_m
        else:
            fin_row = height

        if width > width_m:
            fin_col = width % width_m
        else:
            fin_col = width

        color_m = list()
        color = list()
        count_m = list()
        count = list()
        cube_r = height_m
        cube_c = width_m
        color_num_m = list()
        main_colors_m = list()
        isFirst = True

        for r in range(rows):
            for c in range(cols):
                if r == rows - 1:
                    cube_r = fin_row
                else:
                    cube_r = height_m
                if c == cols - 1:
                    cube_c = fin_col
                else:
                    cube_c = width_m
                num = 0
                for i in range(cube_r):
                    for j in range(cube_c):
                        if num == 0:
                            color_m.append(obj[j+50*c, i+50*r])
                            count_m.append(1)
                            num += 1
                        else:
                            d = num
                            flag = 0
                            cnt = 0
                            while cnt < d and flag == 0:
                                if color_m[cnt] == obj[j+50*c, i+50*r]:
                                    count_m[cnt] += 1
                                    flag = 1
                                cnt += 1

                            if flag == 0:       
                                color_m.append(obj[j+50*c, i+50*r])
                                count_m.append(1)
                                num += 1
                
                for a in range(num):
                    if isFirst and r == 0 and c == 0 and el_num == 0 and count_m[a] >= 100:
                        color.append(copy.copy(color_m[a]))   #Основные цвета
                        colorsNum.append(copy.copy(count_m[a])) #Количество использований основных цветов
                        isFirst = False
                    else:
                        isColor = False
                        sch1 = 0
                        while sch1 < len(color) and not isColor:
                            if math.fabs(color[sch1][0] - color_m[a][0]) <= 30 and math.fabs(color[sch1][1] - color_m[a][1]) <= 30 and math.fabs(color[sch1][2] - color_m[a][2]) <= 30:
                                colorsNum[sch1] += count_m[a]
                                isColor = True
                            sch1 += 1
                        if isColor == False and count_m[a] >= 100:
                            color.append(copy.copy(color_m[a]))   #Основные цвета
                            colorsNum.append(copy.copy(count_m[a])) #Количество использований основных цветов
                
                count_m.clear()
                color_m.clear()

    buf = sorted(colorsNum, reverse = True)
    maxim = buf[0]
    almostMaxim = buf[1]
    for i in range(len(color)):
        if colorsNum[i] == maxim:
            maxNum = i
        if colorsNum[i] == almostMaxim:
            almostMaxNum = i
        #print(color[i], colorsNum[i])

    background = (color[maxNum][0], color[maxNum][1] , color[maxNum][2])
    textColor = (color[almostMaxNum][0], color[almostMaxNum][1] , color[almostMaxNum][2])

    inp = random.randint(0, 1)
    # inp = 0
    if inp == 0:
        #-------------------------------------------------------------------------------Sample1-----------------------------------------------------------------------------
        image = Image.open(path / "Samples" / "Sample2.png") #Открываем изображение. 

        logo = Image.open(logoPath) #Открываем лого. 
        draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 

        widthImg = image.size[0] #Определяем ширину карточки. 
        heightImg = image.size[1] #Определяем высоту карточки.  
        widthLogo = logo.size[0] #Определяем ширину лого. 
        heightLogo = logo.size[1] #Определяем высоту лого.

        koef = float('{:.5f}'.format(widthLogo / heightLogo)) #Коэффицент отношения ширины лого к длине

        #Новые размеры для лого
        if widthLogo > 155 or heightLogo > 160:
            if widthLogo > heightLogo:
                newLSize = (155, math.ceil(155 / koef))  
            else:
                newLSize = (math.ceil(160 * koef), 160) 
            resizedLogo = logo.resize(newLSize)
        else:
            resizedLogo = logo

        #background = color #Цвет фона
        #textColor = (argv[4], argv[5], argv[6]) 

        #Координаты центра логотипа
        xCent = 1000
        yCent = 400

        #Координаты логотипа
        x = 240 #int(xCent - math.ceil(newLSize[0] / 2))
        y = 215 #int(yCent - math.ceil(newLSize[1] / 2))

        #Задаем цвет фона
        for i in range(widthImg):
            for j in range(heightImg):
                draw.point((i, j), background)

        #Вставляем логотип
        image.paste(resizedLogo, (x, y), resizedLogo)

        #------------------------Работа с текстом
        #Главный текст
        txt = "Hello there"
        xText = 1000
        yText = 800
        font_size = 70
        font = ImageFont.truetype(str(path / 'Fonts' / 'DIN Condensed Bold.ttf'), size=font_size)
        w, h = draw.textsize(mainText, font=font)
        xt = 450#int(xText - math.ceil(w / 2))
        yt = 215#int(yText - math.ceil(h / 2))
        draw.text((xt, yt), mainText, textColor, font=font)

        #Слоган
        txt = "Hello"
        xText = 1000
        yText = 800
        font_size = 36
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        w, h = draw.textsize(tagline, font=font)
        xt = 450#int(xText - math.ceil(w / 2))
        yt = 340#int(yText - math.ceil(h / 2))
        draw.text((xt, yt), tagline, textColor, font=font)



        #Сайт
        space = 10 #Отступ сверху
        if siteAddress.find("https://") >= 0:
            txt = siteAddress.replace("https://", "")
        elif siteAddress.find("http://") >= 0:
            txt = siteAddress.replace("http://", "")
        elif siteAddress.find("www.") >= 0:
            txt = siteAddress.replace("www.", "")

        font_size = 28
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        wSite, hSite = draw.textsize(txt, font=font)

         #Телефон
        wPhone, hPhone = draw.textsize(phone, font=font)

        #Почта
        wMail, hMail = draw.textsize(mail, font=font)

        if wSite <= 354:
            xText = 900
            yText = 530
            xtSite = int(xText - math.ceil(wSite / 2))
            ytSite = yText
            draw.text((xtSite, ytSite), txt, textColor, font=font)

            xText = 531
            yText = 530
            xtPhone = int(xText - math.ceil(wPhone / 2))
            ytPhone = yText
            draw.text((xtPhone, ytPhone), phone, textColor, font=font)

            xText = 191
            yText = 530
            xtMail = int(xText - math.ceil(wMail / 2))
            ytMail = yText
            draw.text((xtMail, ytMail), mail, textColor, font=font)
        else:
            xText = 531
            yText = 460
            xtSite = int(xText - math.ceil(wSite / 2))
            ytSite = yText
            draw.text((xtSite, ytSite), txt, textColor, font=font)

            xText = 266
            yText = 530
            xtPhone = int(xText - math.ceil(wPhone / 2))
            ytPhone = yText
            draw.text((xtPhone, ytPhone), phone, textColor, font=font)

            xText = 797
            yText = 530
            xtMail = int(xText - math.ceil(wMail / 2))
            ytMail = yText
            draw.text((xtMail, ytMail), mail, textColor, font=font)
        #------------------------Конец работы с текстом

        #Сохраняем результат
        #finalPath = path / "Samples" / "s1.png"
        img1 = image.save(finalPath, "PNG")
        return finalPath
        #-------------------------------------------------------------------------------Sample1 Ends-----------------------------------------------------------------------------
    elif inp == 1:
        #-------------------------------------------------------------------------------Sample2-----------------------------------------------------------------------------
        image = Image.open(path / "Samples" / "Sample2.png") #Открываем изображение. 
        logo = Image.open(logoPath) #Открываем лого. 
        mask = Image.open(path / "Samples" / "maskSample2.png")
        icons = Image.open(path / "Samples" / "iconsSample2.png")
        drawImg = ImageDraw.Draw(image) #Создаем инструмент для рисования. 
        drawM = ImageDraw.Draw(mask) #Создаем инструмент для рисования. 
        drawIco = ImageDraw.Draw(icons) #Создаем инструмент для рисования. 
        pixM = mask.load()
        pixI = icons.load()

        widthImg = image.size[0] #Определяем ширину карточки. 
        heightImg = image.size[1] #Определяем высоту карточки.  
        widthLogo = logo.size[0] #Определяем ширину лого. 
        heightLogo = logo.size[1] #Определяем высоту лого.

        koef = float('{:.5f}'.format(widthLogo / heightLogo)) #Коэффицент отношения ширины лого к длине

        #Новые размеры для лого
        if widthLogo > 155 or heightLogo > 160:
            if widthLogo > heightLogo:
                newLSize = (155, math.ceil(155 / koef))  
            else:
                newLSize = (math.ceil(160 * koef), 160) 
            resizedLogo = logo.resize(newLSize)
        else:
            resizedLogo = logo

        #background = (argv[1], argv[2], argv[3]) #Цвет фона
        #textColor = (argv[4], argv[5], argv[6]) 

        #Координаты центра логотипа
        xCent = 1000
        yCent = 400

        #Координаты логотипа
        x = 780 #int(xCent - math.ceil(newLSize[0] / 2))
        y = 385 #int(yCent - math.ceil(newLSize[1] / 2))

        #Задаем цвет фона
        for i in range(widthImg):
            for j in range(heightImg):
                drawImg.point((i, j), background)

        #Задаем цвет фона
        for i in range(widthImg):
            for j in range(heightImg):
                if pixM[i, j][3] != 0:
                    drawM.point((i, j), textColor)

        #Задаем цвет фона
        for i in range(widthImg):
            for j in range(heightImg):
                if pixI[i, j][3] != 0:
                    drawIco.point((i, j), background)

        #Вставляем логотип
        image.paste(resizedLogo, (x, y), resizedLogo)
        image.paste(mask, (0, 0), mask)
        image.paste(icons, (0, 0), icons)

        #------------------------Работа с текстом
        #Главный текст
        txt = "Hello there"
        xText = 1000
        yText = 800
        font_size = 60
        font = ImageFont.truetype(str(path / 'Fonts' / 'DIN Condensed Bold.ttf'), size=font_size)
        w, h = drawImg.textsize(mainText, font=font)
        xt = 870 - w#int(xText - math.ceil(w / 2))
        yt = 50#int(yText - math.ceil(h / 2))
        drawImg.text((xt, yt), mainText, textColor, font=font)

        #Слоган
        txt = "Hello"
        xText = 1000
        yText = 800
        font_size = 35
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        w, h = drawImg.textsize(tagline, font=font)
        xt = 870 - w#int(xText - math.ceil(w / 2))
        yt = 105#int(yText - math.ceil(h / 2))
        drawImg.text((xt, yt), tagline, textColor, font=font)

        #Сайт
        space = 10 #Отступ сверху
        txt = "Hello here"
        xText = 1000
        yText = 390
        font_size = 30
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        w, h = drawImg.textsize(siteAddress, font=font)
        xt = 145#int(xText - math.ceil(w / 2))
        yt = int(yText - math.ceil(h / 2))
        drawImg.text((xt, yt), siteAddress, textColor, font=font)

        #Телефон
        space = 10 #Отступ сверху
        txt = "88005553535"
        xText = 1000
        yText = 325
        font_size = 30
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        w, h = drawImg.textsize(phone, font=font)
        xt = 145#int(xText - math.ceil(w / 2))
        yt = int(yText - math.ceil(h / 2))
        drawImg.text((xt, yt), phone, textColor, font=font)

        #Почта
        space = 10 #Отступ сверху
        txt = "mail"
        xText = 1000
        yText = 450
        font_size = 30
        font = ImageFont.truetype(str(path / 'Fonts' / 'trebuc.ttf'), size=font_size)
        w, h = drawImg.textsize(mail, font=font)
        xt = 145#int(xText - math.ceil(w / 2))
        yt = int(yText - math.ceil(h / 2))
        drawImg.text((xt, yt), mail, textColor, font=font)
        #------------------------Конец работы с текстом

        #Сохраняем результат
        #finalPath = path / "Samples" / "s2.png"
        img1 = image.save(finalPath, "PNG")
        return finalPath
        #-------------------------------------------------------------------------------Sample2 Ends-----------------------------------------------------------------------------

#result = runAlg("mainText", "tagline", "https://stackoverflow.com/users/JohnDoe/blablablabla", "88005553535", "bk@mail.ru", "D:\\GitProjects\\vEasytCard\\Scripts\\Samples\\bk.png", "Path")
#print(result)