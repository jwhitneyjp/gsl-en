#!/usr/bin/env python
#-*- encoding: utf8 -*-
'''
    Tools for building resource allocations for use with
    TaskJuggler III.
'''
from nugsl.parsetool import parseSheet
import re,sys,os

team_template = '''
resource team@@teamid@@ "Team @@teamid@@" {@@resources@@
}
'''.rstrip()

resource_template = '''
  resource t@@teamid@@m@@memberid@@ "@@name@@" { limits { dailymax 2h weeklymax 8h } }
'''.rstrip()

macro_template = '''
macro @@macroname@@ [@@macrocontent@@
]
'''.rstrip()

class outputAllocations(parseSheet):

    def __init__(self, filename,
      variexpr='.*語.*チーム.*',
      varilabel='Team',
      varisub='Role'):

        parseSheet.__init__(self, filename,
            variexpr=variexpr,
            varilabel=varilabel,
            varisub=varisub)
            
        self.body = ''
        self.done = []
        
        self.known_expertise = []
        
        #
        # groups is a simple nested list.  [[[<member info>],...],...]
        self.groups = self.get_csv_as_groups() 
        
        user_dir = os.path.expanduser('~')
        template_dir = os.path.join( user_dir, '.nugsl-negotasks' )
        template = 'negotasks.tjp'
        self.template_path = os.path.join( template_dir, template )
        if not os.path.exists( template_dir ):
            os.makedirs( template_dir )
        if not os.path.exists( self.template_path ):
            master_template = os.path.join( '%s', 'share', 'nugsl-negotasks', 'templates', 'negotasks.tjp' )
            master_template = master_template % ( sys.prefix, )
            t = open( master_template ).read()
            open( self.template_path, 'w+' ).write( t )

    def create_teams (self):
        teamid = 1
        teams = ''
        for group in self.groups:
            memberid = 1
            resources = ''
            for member in group:
                resource = resource_template.replace('@@teamid@@', str(teamid))
                resource = resource.replace('@@memberid@@', str(memberid))
                resource = resource.replace('@@name@@', member[2])
                resources += resource
                memberid += 1
            team = team_template.replace('@@resources@@', resources)
            team = team.replace('@@teamid@@', str(teamid))
            teams += team
            teamid += 1
        self.body += teams

        teamid = 1
        macrocontent = ''
        teamids = []
        for group in self.groups:
            teamids.append( str(teamid) )
            teamid += 1
        content = '\n    allocate team' + '\n    allocate team'.join( teamids )
        macro = macro_template.replace('@@macroname@@', 'allocate_teams')
        macro = macro.replace('@@macrocontent@@', content)
        self.body += macro

    def allocate_to_workgroups(self, expertise, tasks ):
        '''
            Feed this function the ID of an expertise (which
            must also be used as a flag against group members in
            the registration spreadsheet), and a list of matters
            to be processed in a round of preparation (an empty
            list will yield an error).
            
            Function will add a complete bundle of allocation
            macros to self.body
        '''
        template = '\n    allocate @@id@@'
        #
        # One expertise only per invocation of this function.
        # Prepare the nested containers for experts and ordinary members
        #
        self.experts = []
        self.nonexperts = []

        if len(self.experts) == 0:
            for group in self.groups:
                self.experts.append( [] )
                self.nonexperts.append( [] )
                for x in range(0,len(tasks),1):
                    self.nonexperts[-1].append( [] )
        gcount = 0
        for group in self.groups:
            count = 0
            for member in group:
                expert_idx = self._csv_data[0].index( 'expertise' )
                if member[ expert_idx ] == expertise and not expertise == 'None':
                    self.experts[ gcount ].append( member[-1] )
                    continue
                if count == len(tasks):
                    count = 0
                self.nonexperts[ gcount ][ count ].append( member[-1] )
                count += 1
            gcount += 1
        
        macros = ''
        #
        # This has to undo the fancy-work of packing nonexperts
        # into subgroups.
        if not expertise == 'None' and not expertise in self.known_expertise:
            self.known_expertise.append( expertise )
            nontaskname = 'allocate_non%ss' % (expertise,)
            macro = macro_template.replace('@@macroname@@', nontaskname)
            commands = ''
            for subgroup in self.nonexperts:
                for group in subgroup:
                    for memberid in group:
                        macroline = template.replace('@@id@@', memberid)
                        commands += macroline
            macro = macro.replace('@@macrocontent@@', commands)
            macros += macro

        count = 0
        for speciality in tasks:
            if expertise == 'None':
                taskname = 'allocate_%s' % (speciality, )
            else:
                taskname = 'allocate_non%s_%s' % (expertise, speciality)
                
            macro = macro_template.replace('@@macroname@@', taskname)
            commands = ''
            for nonexpert in self.nonexperts:
                for memberid in nonexpert[ count ]:
                    macroline = template.replace('@@id@@', memberid)
                    commands += macroline
            macro = macro.replace('@@macrocontent@@', commands)
            macros += macro
            count += 1
        
        if not expertise == 'None':
            speciality_names = '_'.join( tasks )
            macroname = 'allocate_%s_%s_briefing' % (expertise, speciality_names)
            macro = macro_template.replace('@@macroname@@', macroname)
            gcount = 0        
            macrocontent = ''
            for group in self.groups:
                gexpertstring = ', '.join(self.experts[ gcount ])
                macroline = '\n    allocate ' + gexpertstring
                count = 0
                macrolinesupp = []
                alternatives_template = '%s { alternative %s select minallocated persistent }'
                for speciality in tasks:
                    gspecialistone = self.nonexperts[ gcount ][ count ][0]
                    gspecialistothers = ', '.join(self.nonexperts[ gcount ][ count ][1:])
                    if gspecialistothers:
                        supp = alternatives_template % (gspecialistone, gspecialistothers)
                    else:
                        supp = gspecialistone
                    macrolinesupp.append( supp )
                    count += 1
                macroline += ', ' + ', '.join( macrolinesupp )
                macrocontent += macroline
                gcount += 1
            macro = macro.replace('@@macrocontent@@', macrocontent)
            macros += macro
        
            ## Generate expert macros here if required
            if not expertise in self.done:
                macroname = 'allocate_%ss' %expertise
                macro = macro_template.replace('@@macroname@@', macroname)
                macrocontent = ''
                for expert in self.experts:
                    for member in expert:
                        macrocontent += '\n    allocate %s' %member
                macro = macro.replace( '@@macrocontent@@', macrocontent )
                macros += macro
                if not expertise in self.done:
                    self.done.append( expertise )
            
        self.body += macros

    def get_csv_as_groups(self):
        csv = self._csv_data
        group_idx = csv[0].index( self.varilabel )
        csv[0].append('tjid')
        groups = []
        group = []
        teamid = 1
        memberid = 1
        prev = self._csv_data[1][group_idx]
        for line in self._csv_data[1:]:
            if prev != line[group_idx]:
                groups.append( group )
                group = []
                prev = line[group_idx]
                teamid += 1
                memberid = 1
            myline = line[:]
            myid = 't%sm%s' % (teamid,memberid)
            myline.append(myid)
            group.append( myline )
            memberid += 1
            
        groups.append( group )
        return groups

    def merge(self):
        sub = '\\1' + self.body + '\n\\3'
        ispec = open( self.template_path ).read()
        rex = re.compile('(## Allocations start ##)(.*)(## Allocations end ##)',re.M|re.S)
        ospec = re.sub(rex, sub, ispec)
        open('./negocomp.tjp','w+').write(ospec)
