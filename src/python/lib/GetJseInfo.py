#-*- encoding: utf-8 -*-
'''
  Module for extracting information on the Japanese website
  that can be refactored for use on the English site.
'''

def getJseUpdate(doc):
        ret = {}
        cites_as_string = ''
        #path = doc.xpathEval('//dl[dt = "主要著作"]/dd')
        path = doc.xpathEval('//h4[text() = "主要著作"]/following-sibling::*[self::div or self::p][1]')
        if path and path[0].get_name() == 'p':
            for p in path:
                #
                # Strip tags and normalize to Unicode
                cites = p.serialize()[3:-4].decode('utf8','replace')
                #
                # Split at line breaks to get individual citations
                cites = cites.split('<br>')
                #
                # Action only if citation exists
                for x in cites:
                    cite = x.strip()
                    if cite:
                        cites_as_string = cites_as_string + cite + '\n'
        ret['Jpublications'] = cites_as_string
        
        posts_as_string = ''
        path = doc.xpathEval('//h4[text() = "略歴"]/following-sibling::p[1]')
        for p in path:
            #
            # Strip tags and normalize to Unicode
            posts = p.serialize()[3:-4].decode('utf8','replace')
            #
            # Split at line breaks to get individual citations
            posts = posts.split('<br>')
            #
            # Action only if citation exists
            for x in posts:
                post = x.strip()
                if post:
                    posts_as_string = posts_as_string + post + '\n'
        ret['Jcareer_history'] = posts_as_string
        
        memberships_as_string = ''
        path = doc.xpathEval('//h4[text() = "所属学会"]/following-sibling::p[1]')
        for p in path:
            #
            # Strip tags and normalize to Unicode
            memberships = p.serialize()[3:-4].decode('utf8','replace')
            #
            # Split at line breaks to get individual citations
            memberships = memberships.split('<br>')
            #
            # Action only if citation exists
            for x in memberships:
                membership = x.strip()
                if membership:
                    memberships_as_string = memberships_as_string + membership + '\n'
        ret['Jmemberships'] = memberships_as_string
        
        return ret

# Tidy up a Unicode Japanese name
def normalizeJseName(name):
    name = name.replace(unichr(12288),'')
    name = name.replace(unichr(32),'')
    name = name.replace('（仮）'.decode('utf8'),'')
    name = name.replace('准教授'.decode('utf8'),'')
    name = name.replace('教授'.decode('utf8'),'')
    return name

# Take site index page doc object as argument
def getJseUrls(webdoc):
    # Get a list of potential staff names from the
    # page
    l = []
    res = webdoc.xpathEval('//h4/following-sibling::ul/li//a')
    for r in res:
        if r.prop('href'):
            name = r.content.decode('utf8')
            name = name.replace(unichr(12288),'')
            name = name.replace(unichr(32),'')
            l.append((name,r.prop('href')))
    
    prof_j_url = {}
    for i in l:
        prof_j_url[i[0]] = i[1]

    return prof_j_url
