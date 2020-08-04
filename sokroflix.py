# -*- coding:utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 12 created 02/08/2020

import re
import string
import json
import sys
#import time #
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import  xbmc
 
from resources.lib.comaddon import  VSlog
bVSlog=False


SITE_IDENTIFIER = 'sokroflix'
SITE_NAME = 'Sokroflix'
SITE_DESC = 'Films, Séries en streaming'

URL_MAIN = 'https://w6.sokroflix.com/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

#recherche globale MOVIE/TVSHOWS
key_search_movies='#searchsomemovies'
key_search_series='#searchsomeseries'
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')

MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

MOVIE_MOVIES = (URL_MAIN + 'filmstreaming/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'notes/?get=movies', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_ALPHA = (True, 'showAlphaMovies')

SERIE_SERIES = (URL_MAIN + 'seriestreaming1', 'showMovies')
SERIE_TOP = (URL_MAIN + 'notes/?get=tv', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'tendance/?get=tv', 'showMovies') # trouve
SERIE_ALPHA = (True, 'showAlphaSeries')

SERIE_NEWS_SAISONS = (URL_MAIN + 'saisons/', 'showMovies')
SERIE_NEWS_EPISODES= (URL_MAIN + 'episodes/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/page/1/', 'showMovies') # !!! page /1/ pour le next page

# on rajoute quelque genre qui sont un type au meme titre que film serie 
TELEFILM_TELEFILMS=(URL_MAIN +'/genre/telefilm/page/1/', 'showMovies')
ANIMATION_ANIMATIONS=(URL_MAIN +'/genre/animation/page/1/', 'showMovies')
ANIME_ANIMES=(URL_MAIN +'/genre/anime/page/1/', 'showMovies')

# le site n'est pas a jour sur ses pages on desactive les menus
bADD_Dir_SERIE_NEWS_SAISONS = False
bADD_Dir_SERIE_NEWS_EPISODES = False


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesMenu', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesMenu', 'Séries', 'series.png', oOutputParameterHandler)
    
    #oGui.addText(SITE_IDENTIFIER, '>')
    # pas indispenspensabe on ajoute le genre telefilms
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TELEFILM_TELEFILMS[0])
    oGui.addDir(SITE_IDENTIFIER, TELEFILM_TELEFILMS[1], 'Télefilms', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIMATION_ANIMATIONS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIMATION_ANIMATIONS[1], 'Films Animation ', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_ANIMES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_ANIMES[1], 'Series Animes', 'genres.png', oOutputParameterHandler)
    
    #oGui.addText(SITE_IDENTIFIER, '>')
    
    
    
    
    oGui.setEndOfDirectory()


def showMoviesMenu():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0] )
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIES[1], 'Tous les Films ', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films (Top)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus populaires)', 'films.png', oOutputParameterHandler)
    
    # semble ne renvoyer que des films
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Series (Par Genres)', 'genres.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films(Par Genres)', 'genres.png', oOutputParameterHandler)
    # semble ne renvoyer que des films
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films & Series (Par années)', 'annees.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALPHA[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler) 

    
    oGui.setEndOfDirectory()


def showSeriesMenu():
    
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0] )
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Toutes les Séries ', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TOP[1], 'Séries (Top)', 'notes.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (les plus populaires)', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries (NETFLIX)', 'series.png', oOutputParameterHandler)
    
    if bADD_Dir_SERIE_NEWS_SAISONS:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_SAISONS[0])
        oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_SAISONS[1], 'Séries (Saison Récentes)', 'news.png', oOutputParameterHandler)

    if bADD_Dir_SERIE_NEWS_EPISODES:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODES[0])
        oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODES[1], 'Séries (Episodes Recents)', 'news.png', oOutputParameterHandler)
        
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ALPHA[1], 'Séries (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()

def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    
def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0]+ key_search_movies + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    

def showGenres():
    
    oGui = cGui()
    #
    #href="https://w6.sokroflix.com/genre/aventure/
    liste = []
    listegenre=['action-adventure','animation','anime','aventure',
                'comedie', 'crime', 'documentaire','drame',
                'familial','fantastique','guerre','histoire','horreur',
                'kids','musique','mystere','reality','romance'
                ,'science-fiction','science-fiction-fantastique','soap'
                ,'talk','telefilm','thriller','war-politics','western']
    
    url1g= URL_MAIN + 'genre/'
   
    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre  ])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def showMovieYears():
    oGui = cGui()
    #  peu creer bug bloquant  si année < a la date indiquée ds page!!! pattern au choux ?????
    #  on va risquer comme meme car le site possede pas mal de vieux films et faut pas s'en priver
    for i in reversed(range(1930, 2021)): # utiliser (range(1971, 2021)) pour aucun bug
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'sortie/' + Year +'/page/1/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlphaMovies():
    showAlpha('movies')
    
def showAlphaSeries() :
    showAlpha('tvshows')#req serie trouvée  : requete non mis sur sites

def showAlpha(stype):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #requete json 20 resultat max
    #https://mystream.zone/wp-json/dooplay/glossary/?term=g&nonce=2132c17353&type=tvshows
    
    url1='https://mystream.zone/wp-json/dooplay/glossary/?term='
    url2='&nonce='
    snonce='2132c17353'  # a surveiller si jamais cela change
    url3='&type='
    
    #https://w6.sokroflix.com/wp-json/dooplay/glossary/?term=f  #f=str(alpha)
    #&nonce=
    #ff2aa98f98&type=movies
    
    
    url1= URL_MAIN +'wp-json/dooplay/glossary/?term='
    url2='&nonce='
    snonce='ff2aa98f98'
    
    sAlpha= string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = []
    for alpha in listalpha :
        liste.append([str(alpha).upper(),url1+str(alpha) + url2 + snonce +url3+stype])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies(sSearch=''):
    oGui = cGui()
    #ifVSlog('countg='+str(countg))
    ifVSlog('#')
    ifVSlog('showMovies')
    
    bkSearchMovie=False
    bkSearchSerie=False 
    if sSearch:
        sUrl = sSearch.replace(' ', '%20')
        ifVSlog('url request before =' + sUrl)
        if key_search_movies in sUrl :
            sUrl=str(sUrl).replace( key_search_movies , '')
            bkSearchMovie=True  
        if key_search_series in sUrl :
            sUrl=str(sUrl).replace( key_search_series , '')
            bkSearchSerie=True
    
        ifVSlog('url request After =' + sUrl)
    
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    ifVSlog('url request  =' + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #no desc
    if 'wp-json' in sUrl and not sSearch: #json req : term=alpha + type=tvshows or type=movies
        oRequestHandler = cRequestHandler(sUrl)
        #oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3') 
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
        ifVSlog(str(jsonrsp ))
        for i, idict in jsonrsp.items():    
            #sTitle=str(jsonrsp[i]['title'].encode('utf-8', 'ignore'))  #I Know This Much Is True mystream
            #sTitle=str(jsonrsp[i]['title'] .encode('utf-8', 'ignore'))
            sTitle=str(jsonrsp[i]['title'] .encode('utf-8', 'replace'))
            sUrl2=str(jsonrsp[i]['url'])
            sThumb=str(jsonrsp[i]['img'])
            sYear='YYYY'
            try:
                sYear=str(jsonrsp[i]['year'])
            except:
                pass        
            #VSlog('response url2 '+ sUrl2)
            ifVSlog('name = '+ sTitle)
            ifVSlog('url = ' + sUrl2 )
            #ifVSlog('sThumb= ' + sThumb )
            ifVSlog('syears = ' + sYear)
            sDisplayTitle = sTitle + ' (' + sYear + ')'
            sDesc = ''
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            #if 'type=tvshows' in sUrl:#/seriestreaming1/'
            if '/seriestreaming1/' in sUrl2:   
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            if '/filmstreaming/'  in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)    

            else:
                ifVSlog(' :showAlpha :wp-json : Cannot add a folder for url  =' + sUrl) 
                
                #oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        #  1 seul resultat de 18 elements max
        oGui.setEndOfDirectory()
        return
    
    ##href="https://w6.sokroflix.com/genre/action/                  #desc_category # decoupage string unique ds page
    #https://w6.sokroflix.com/sortie/2013/                          #desc_category
    #href="https://w6.sokroflix.com/filmstreaming/page/2/           #<h1>Films</h1>
    #href="https://w6.sokroflix.com/seriestreaming1/page/2/" />     #<h1>Séries</h1>
    if '/genre/' in sUrl or '/sortie/' in sUrl or 'filmstreaming' in sUrl or 'seriestreaming' in sUrl or 'netflix' in sUrl:
        # url title years desc thum
        startString=''
        
        #img title ref years desc
        sPattern = '<img src="([^"]*).*?alt="([^"]*).+?href="([^"]*)".+?<span>+?([\d]*)<.span.+?"texto">([^<]*)'
        if 'filmstreaming' in sUrl :
            startString='<h1>Films</h1>'
        
        elif 'seriestreaming' in sUrl:
            startString='<h1>Séries</h1>'
            
        else:
            startString='desc_category'    
               
        sHtmlContent=sHtmlContent[sHtmlContent.find( startString ):sHtmlContent.find('application/javascript')]
        if  not sHtmlContent :
            ifVSlog( 'no find start and end string in sHtmlContent')
            oGui.setEndOfDirectory()
            return
            
    elif '?get=tv' in sUrl or '?get=movies' in sUrl : # pas de desc
        # sPattern :compatible
        #view-source:https://w6.sokroflix.com/notes/ # non fait film et serie
        #view-source:https://w6.sokroflix.com/tendance/ # non fait film et serie
        # 
        #https://w6.sokroflix.com/tendance/?get=tv
        #https://w6.sokroflix.com/tendance/?get=movies
        #https://w6.sokroflix.com/notes/?get=movies
        #https://w6.sokroflix.com/notes/?get=tv
        
        # thum title url years
        sPattern = '<article id=.+?src="([^"]*).+?alt="([^"]*).+?ref="([^"]*).*?span>.*?([\d]*)<'
    
    elif '/saisons/' in sUrl: #image  url   number title 
        sPattern = 'item se seasons.+?src="([^"]*)".+?href="([^"]*).+?class="b">([^<]*).+?c">([^<]*)'
    
    elif '/episodes/' in sUrl: #url 'S1.E1.'  years '.2020'   title img
        sPattern = 'div class="season_m.+?data.+?href="([^"]*)"..+?span>([^\/]*).+?,([^<]*).+?serie">([^<]*).+?src="([^"]*)"'

    
    
    elif sSearch:
        #  url thumb title years desc
        sPattern = 'class="thumbnail.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]*).+?class="year">([^<]*).+?<p>([^<]*)'
    
    else:  #Non traité
        #https://w6.sokroflix.com/notes/
        #https://w6.sokroflix.com/tendance/
        #hhttps://w6.sokroflix.com/episodes/
        #https://w6.sokroflix.com/saisons/  
        ifVSlog(' cannot select a pattern  for  =' + sUrl)
        oGui.addText(SITE_IDENTIFIER, '[COLOR red] URL inconnue  [/COLOR]')
        oGui.setEndOfDirectory()
        return
    
    #ifVSlog('sel pattern='+ sPattern)
    #ifVSlog('try parse' ) # !!! tres tres gros blocage de l'application kodi si pattern au choux
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #ifVSlog('end parse' )
 
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        #ifVSlog(sHtmlContent)
        ifVSlog('')
        ifVSlog('Failed Pattern with url = '+sUrl )
        ifVSlog('Selected Pattern = ' +sPattern )
        
    if (aResult[0] == True):
        sDisplayTitle=""
        for aEntry in aResult[1]:
            if  '/genre/' in sUrl or '/sortie/' in sUrl or 'filmstreaming' in sUrl or 'seriestreaming' in sUrl or 'netflix' in sUrl:
                #img title ref years desc
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
                sYear = aEntry[3]
                sDesc = aEntry[4]
                #  descrpitions inutiles: ou faire if 'resumé' in desc
                #sDesc=str(sDesc).replace('Voir film streaming streaming', '').replace('Vous allez aimer voir film streaming.', '')
                sDisplayTitle = sTitle + ' (' + sYear  + ')' 
                
                # les réponses aux requetes genre et années ne semblent ne donner que des  films mais on peu verifier..... ou pas
                if False :
                    if  '/genre/' in sUrl or '/sortie/'  in sUrl  :
                        if '/filmstreaming/' in sUrl2 :
                            sDisplayTitle= sDisplayTitle + ' [movie]'
                        else:
                            sDisplayTitle= sDisplayTitle + ' [serie]'
        
            elif '?get=tv' in sUrl or '?get=movies' in sUrl : #thum title url years
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
                sYear = aEntry[3]
                sDesc = ''
                sDisplayTitle=sTitle
            
            elif  '/saisons/' in sUrl : #  image  url number title   
                sUrl2 =aEntry[1]
                sTitle = aEntry[3] 
                sThumb= aEntry[0]
                sDisplayTitle= sTitle + ' Saison ' + aEntry[2]
                sYear = ''
                sDesc = ''
            
            elif '/episodes/' in sUrl: # url ;'S1.E1.' ; years '.2020' ;  title; img
                sUrl2 =aEntry[0]
                sTitle = aEntry[3]  + ' ' + aEntry[1] 
                sThumb= aEntry[4]
                sDisplayTitle= sTitle  + '('+ aEntry[2]  +')'
                sYear= aEntry[2]
                sDesc = ''
            

            elif sSearch : # url thumb title yeras desc
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sYear = aEntry[3]
                sDesc = aEntry[4]
                sDisplayTitle=sTitle
                #Voir film streaming streaming Vous allez aimer voir film streaming.
                #sDesc=str(sDesc).replace('Vous allez aimer voir film streaming.', '')
                #sDesc=str(sDesc).replace('Voir film streaming streaming Résumé Sokroflix de streaming', '[COLOR coral] SYNOPSIS [/COLOR] ')
                
                #recherche avec films et serie on tag alors pour distinguer la recherche
                if (not bkSearchMovie) and (not bkSearchSerie) : 
                    if '/filmstreaming/' in sUrl2 :
                        sDisplayTitle= sDisplayTitle + ' [movie]'
                    else:
                        sDisplayTitle= sDisplayTitle + ' [serie]'

            else:  #c'est mal progammé pas tous les cas gérés
                ifVSlog('erreur de programmation  =' + sUrl)
                oGui.addText(SITE_IDENTIFIER, '[COLOR red] erreur de programmation   [/COLOR]')
                oGui.setEndOfDirectory()

            #  filtre 
            if bkSearchMovie :
                if '/seriestreaming1/' in sUrl2 :
                    continue  
            if bkSearchSerie :
                if '/filmstreaming/' in sUrl2 :
                    continue
            
            ifVSlog('name = '+ sTitle)
            ifVSlog('url = ' + sUrl2 )
            #ifVSlog('sThumb= ' + sThumb )
            ifVSlog('desc = ' + sDesc )
            sDesc=cleanDesc(sDesc)
            ifVSlog('clean sdesc = ' + sDesc )
            
            
            #ifVSlog('syears= ' + sYear)
            
            
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
      
            if '/seriestreaming1/' in sUrl2:
                ifVSlog('ADD TV ; showSaisons')
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            
            #  pages pourries de liens  vides.... voir si next page plus de liens valable
            elif  '/saisons/' in sUrl2:
                ifVSlog('ADD TV ; ShowEpisodes')
                oGui.addTV(SITE_IDENTIFIER, 'ShowEpisodes', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            
            elif '/filmstreaming/' in sUrl2 or '/episodes/' in sUrl2:
                ifVSlog('ADD Movie ; showLink')
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)
            
            else:
                ifVSlog('Cannot add a folder for url  =' + sUrl)
                
        bNextPage,urlNextpage,pagination  = __checkForNextPage(sHtmlContent,sUrl)
        if (bNextPage ):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlNextpage) 
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)
      
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent,sUrl):
    
    #ifVSlog('checkForNextPage: ' )
    oParser = cParser()
    bnext=False
    urlNextpage=''
    snumberNext=''
    sNumberMax=''

    sPattern = 'class="pagination"><span>.*?([\d]*)<.span'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False): 
        #ifVSlog(' pagination failed...exit' ) #  peu etre normale
        return False ,urlNextpage, 'nothing'   
    if (aResult[0] == True):   
        sNumberMax=aResult[1][0]
        
    sPattern = 'class=.arrow_pag.+?ref="([^"]*)".+?id=.nextpagination'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False): 
        #ifVSlog('pattern urlNextpage failed ;' + sUrl) # peu etre normale
        if sNumberMax:
            try:
                snumbercurrent = re.search('/page/([0-9]+)', sUrl ).group(1)
                inumbercurrent = int(snumbercurrent)
                if  inumbercurrent <= int(sNumberMax): #bug voir decalage ex 6/5 >>
                    inumberNext = inumbercurrent +1
                    snumberNext = str(inumberNext)
                    sreplaceold = '/'+ snumbercurrent +'/'
                    sreplacenew = '/'+ snumberNext +'/'
                    urlNextpage = str(sUrl).replace(sreplaceold, sreplacenew)
                    #ifVSlog(' created urlNextpage with current url ='+urlNextpage )
            except:
                ifVSlog('exception : cannot created next page  with sUrl' + sUrl) #voir si possible avec gere talk 1 resulta 
                return False ,'no urlNextpage', 'no pagination'
                pass           
    
    if (aResult[0] == True):#page.([\d]*).
        urlNextpage= aResult[1][0]
        snumberNext = re.search('/page/([0-9]+)', urlNextpage ).group(1)
        #ifVSlog('Find urlNextpage in shtml url ='+urlNextpage )
        try:
            inumbercurrent=int(snumberNext)-1
        except: #  pas grave 
            pass

    #ifVSlog(urlNextpage)
    #ifVSlog(snumberNext)
    #ifVSlog(sNumberMax)
    
    #pagination='Page ' + snumberNext +'/'+sNumberMax+' '
    
    #affiche : page courante / max page
    if inumbercurrent:
        pagination='Page ' + str(inumbercurrent) +'/'+sNumberMax
        return True ,urlNextpage, pagination 
        
    #ffiche nextpage/ max page  (mais avec bug a la derniere page=max , ex:page max=2 donne page 3/2 >>>)
    if urlNextpage :
        pagination='Page ' + snumberNext +'/'+sNumberMax
        return True ,urlNextpage, pagination     
    
    ifVSlog('erreur de programme page next non trouvée') #
    return False ,urlNextpage, 'no pagination'


def showSaisons():
    #parent https://mystream.zone/tvshows/
    #parent https://mystream.zone/tendance/
    oGui = cGui() 
    ifVSlog('#')
    ifVSlog('showSaisons()')

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc= oInputParameterHandler.getValue('sDesc')
    sTitle= oInputParameterHandler.getValue('sMovieTitle')
    sYear= oInputParameterHandler.getValue('sYear')
    
    sMenu= oInputParameterHandler.getValue('sMenu')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #  on  passe ts les liens  des épisodes dans chaque dossier saisons créés ds un liste 
    #  car pas de liens existants ds la page pour acceder aux pages de chaque saison
    #  meme cas mystream.py 
    
    if True:
        try:
            sPattern = 'Synopsis<.h2>.*?Résumé.*?<p>([^<]*)' # desc coupé mais trop long
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            #ifVSlog('Try exception ')
            pass
    #  '2 - 11'   href   title
    #class='numerando'>([^<]*).+?href='([^']*).>([^<]*) #
    sPattern = "class='numerando'>([^<]*).+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        ListNumeroSaison=[]
        listeUrlEpisode=[]
        listeStitle=[]
        titlesaison=''
        icurrentsaison=0
        #timestart= int(time.time())
        for aEntry in aResult[1]:
            ifVSlog('sTitle ='+sTitle )#ok
            ifVSlog(aEntry[0])  # debug si pb episode
            
            
            iSaison = re.search('([0-9]+)', aEntry[0]).group(1)
            iEpisode= re.search('([0-9]+)$', aEntry[0]).group(1)
            if not str(iSaison) in ListNumeroSaison :
                ListNumeroSaison.append(str(iSaison))
                sTitleDisplay=sTitle +' '+ 'Saison' + ' '+ str(icurrentsaison )
                if sYear:
                    sTitleDisplay= sTitleDisplay + ' (' + sYear + ' )' 

                if len(listeUrlEpisode) >0: 
                    #order :  saison number  descending 
                    ifVSlog('ADD list Episodes to Saison'+ str(icurrentsaison))
                    ifVSlog('ADD Episode,ListEpisodes'+str(listeStitle))
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oOutputParameterHandler.addParameter('listeUrlEpisode', listeUrlEpisode)
                    oOutputParameterHandler.addParameter('listeStitle', listeStitle)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showListEpisodes', sTitleDisplay, '', sThumb, sDesc, oOutputParameterHandler)
                    listeUrlEpisode=[]
                    listeStitle=[]            
                icurrentsaison=iSaison  

            listeUrlEpisode.append(str(aEntry[1]) )
            sTitleEp =  sTitle +' '+ ' Saison ' + str(iSaison ) + ' Episode ' + str(iEpisode) # bug
            sTitleEp=changeChar(sTitleEp)
            
            #sTitleEp=sTitleEp.decode('utf-8')
            
            #ifVSlog('before handle line sTitleEp = '+sTitleEp)
            #sTitleEp=handleLine(sTitleEp)
            #ifVSlog('After handle line sTitleEp = '+sTitleEp)
            
            ifVSlog('sTitleEp = '+sTitleEp) # affiche ok mais naze comme meme
            
            listeStitle.append(sTitleEp ) # bug decode
            sTitleDisplay=sTitle +' '+ 'Saison' + ' '+ str(iSaison )
            if sYear:
                sTitleDisplay= sTitleDisplay + ' (' + sYear + ' )' 
        #timestop= int(time.time())    
        #timespan=timestop-timestart
        #ifVSlog('End showSaisons():Totaltime  :'+str(timespan))# temps <1s
        
        # on ajoute ici le dernier
        ifVSlog('ADD list Episodes to Saison'+ str(iSaison))
        ifVSlog('ADD showEpisodes'+str(listeStitle))         #bug ADD showEpisodes ['Coraz\xc3\xb3n Partido  Saison 1 Episode 90',
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('listeUrlEpisode', listeUrlEpisode)
        oOutputParameterHandler.addParameter('listeStitle', listeStitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showListEpisodes', sTitleDisplay, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showListEpisodes():
    #parent https://mystream.zone/tvshows   
    oGui = cGui()
    #ifVSlog('#')
    ifVSlog('showListEpisodes()')

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear= oInputParameterHandler.getValue('sYear')
    listeUrlEpisode = oInputParameterHandler.getValue('listeUrlEpisode')
    listeStitle = oInputParameterHandler.getValue('listeStitle')

    listeUrlEpisode2=[]
    listeStitle2=[]
    sPattern="'([^']*)'"
    oParser = cParser()

    aResult = oParser.parse(listeUrlEpisode, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            listeUrlEpisode2.append(aEntry)

    aResult = oParser.parse(listeStitle, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            #ifVSlog('title' + aEntry)
            listeStitle2.append(aEntry)              

    #for itemurl in listeUrlEpisode2 :
        #sTitle=listeStitle2[i]
        #i=i+1
    #re order for menu: episode number ascending
    lenlist=len(listeUrlEpisode2)
    i=0
    for itemurl in listeUrlEpisode2 :
        sTitle=listeStitle2[(lenlist-1)-i]
        url=listeUrlEpisode2[(lenlist-1)-i]
        i=i+1
 
        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('siteUrl',itemurl ) # reverse order
        oOutputParameterHandler.addParameter('siteUrl',url )    #  order
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowEpisodes():
    #  utilises : mais pas fait !!! (menu episode desactive)
    
    
    oGui = cGui() 
    ifVSlog('#')
    ifVSlog('ShowEpisodes()')

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc= oInputParameterHandler.getValue('sDesc')
    sTitle= oInputParameterHandler.getValue('sMovieTitle')
    sYear= oInputParameterHandler.getValue('sYear')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    
    if "Il n'y a pas encores d'épisodes pour cette saison" in sHtmlContent :
        oGui.addText(SITE_IDENTIFIER,"sokroflix.com : Il n'y a pas encores d'épisodes pour cette saison")
        oGui.setEndOfDirectory()
        return

    if not sDesc:
        try:
            sPattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            #ifVSlog('Try exception ')
            pass
    #  thumb '2 - 11'   url  
    sPattern = "class='imagen'.+?src='([^']*).*?class='numerando'>([^<]*).+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        oGui.addText(SITE_IDENTIFIER)
        #ifVSlog(sHtmlContent)
        ifVSlog('')
        ifVSlog('Failed Pattern with url = '+sUrl )
        ifVSlog('Selected Pattern = ' +sPattern )
        oGui.setEndOfDirectory()
        return

    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            iSaison = re.search('([0-9]+)', aEntry[1]).group(1)
            iEpisode= re.search('([0-9]+)$', aEntry[1]).group(1)
            sUrl=aEntry[2]
            sTitleDisplay=sTitle+' '+ ' Saison ' + str(iSaison ) + ' Episode ' + str(iEpisode)
            
            #if sYear:
                #sTitleDisplay= sTitleDisplay + ' (' + sYear + ' )'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitleDisplay)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitleDisplay , '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showLink():
    oGui = cGui()
    oParser = cParser()
    ifVSlog('#')
    ifVSlog('showLink')
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl= oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc= oInputParameterHandler.getValue('sDesc')
    sYear= oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    ifVSlog('url ='+sUrl)
    try:
        
        sPattern = 'R*?streaming.*?<p>([^<]*)'
        #1 match 2 groupes resume desc
        aResult = oParser.parse(sHtmlContent, sPattern)
        ifVSlog(str(aResult ))
        if aResult[0]:
            sDesc = aResult[1][1]
        else:    
            ifVSlog('cannot update sDesc ')
    except:
        ifVSlog('Try exception sDesc ')
        pass
    
    sPattern = "data-type='([^']*).*?post='([^']*).*?nume='([^']*).*?title'>([^<]*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            datatype=aEntry[0]
            datapost=aEntry[1]
            datanum=aEntry[2]
            sUrl2='https://w6.sokroflix.com/wp-admin/admin-ajax.php'#URL_MAIN
            sUrl2= URL_MAIN +'wp-admin/admin-ajax.php'
           
            pdata = 'action=doo_player_ajax&post=' + datapost + '&nume=' + datanum + '&type=' + datatype
            ifVSlog(' pdata = ' + pdata )
            
            sDisplayTitle= ('%s [COLOR coral]%s[/COLOR]') % (sTitle , aEntry[3])
            if sYear:
                sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle  + ' (' + sYear  + ')', aEntry[3])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('pdata',pdata )
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    #ifVSlog('#')
    ifVSlog('Hosterslink ()')

    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    referer = oInputParameterHandler.getValue('referer')
    pdata=oInputParameterHandler.getValue('pdata')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear= oInputParameterHandler.getValue('sYear')
    #if sYear :
        #sMovieTitle= sMovieTitle + ' (' + sYear + ' )'   

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    #oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    #oRequest.addHeaderEntry('Accept', '*/*')
    #oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    #oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)
    sHtmlContent = oRequest.request()
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")' # c'est à cezar 
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            
            ifVSlog('ADD Host : sHosterUrl='+str(sHosterUrl)) 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()

  
def cleanDesc(sdesc):
    list_comment=[
                'streaming HD sur Sokroflix Résumé de la serie  streaming HD sur Sokroflix:'
                , 'Voir film streaming streaming Résumé Sokroflix de streaming :'
                , ' Vous allez aimer voir film streaming.'
                , 'Voir Serie streaming sur Sokroflix Résumé de la serie streaming sur Sokroflix:'
                , 'Voir serie  '
                , 'Voir serie streaming sur Sokroflix Résumé de la serie streaming sur Sokroflix:'
                , 'Bonne soirée avec la serie streaming sur Sokroflix.' 
                ]
        
    for s in list_comment :
        sdesc=sdesc.replace(s , '')
    return sdesc

def changeChar(sStr):
   
    sStr=sStr.replace('ó', 'o').replace('é', 'e').replace('è', 'e').replace('', '')\
    .replace('â', 'a').replace('ê', 'e').replace('î', 'i').replace('ô', 'o').replace('à', 'a')
    
    
    return sStr
   


def ifVSlog(log):
    if bVSlog:
        try:  # si no import VSlog from resources.lib.comaddon
            VSlog(str(log)) 
        except:
            pass
