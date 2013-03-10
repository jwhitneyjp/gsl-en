#!/usr/bin/python
#-*- encoding: utf8 -*-

import sys,os,re,copy

# Constants


class disAmbiguate:
    ''' Resolve ambiguities in digit strings returned by OCR.
    
        Page cleaning done in connection with optical character
	recognition frequently removes commas together with undesired
	page clutter.  This module provides methods for repairing this
	damage.  When ambiguities cannot be resolved on the basis of
	the known text, it may be necessary to return multiple,
	alternative versions of a page.
    '''
    
    def __init__(self):
        self.i_give_up = False
        #
        # Wworking list
        #
        self.wrk = []

    def combine_tokens(self):
        ''' Safely combine tokens, watching for ambiguity
        
            Given a list of string tokens WRK in the reverse
            of visual order, attempt to 
        
            Combine tokens, starting from the small end of the 
	    original number string.  If the small-end value is 
	    smaller than the remaining string of digits taken as one
	    number, merge it with the next. When the small-end value
	    grows equal to or larger than the remaining string, we
	    have an ambiguity.  Ambiguous cases return a tuple rather
            than a string.
            
            The working list is always empty when this method exits.
        '''
            
        while len(self.wrk) > 1:
            current = self.wrk[0].replace(',','')
            other = self.wrk[1:]
            other.reverse()
            other = ''.join([x.replace(',','') for x in other])
            
            if int(current) < int(other):
                self.wrk[0] = self.wrk[1] + ',' + self.wrk[0]
                self.wrk.pop(1)
            else:
                break
        if len(self.wrk) > 1:
            self.wrk.reverse()
            possibilities = []
            for pos in range(len(self.wrk)-1,-1,-1):
                first  = self.wrk[0:pos]
                second = self.wrk[pos:len(self.wrk)]
                possibility = ' '.join([','.join(first), ','.join(second)] ).strip(' ')
                possibilities.append( possibility )
            self.wrk =  [tuple(possibilities)]
        ret = self.wrk[0]
        self.wrk = []
        return ret

    def disambiguate(self, txt):
        #
        # Start by extracting suspect runs of numbers
        # to a token list.
        #
        NUMS = '[0-9][, 0-9]* [, 0-9]*[0-9]'
        nums = re.findall(NUMS,txt)
        #
        # Then replace them with placeholders in the text.
        #
        txt = re.sub(NUMS,'@@NUM@@',txt)
        txt = re.split('@@NUM@@',txt)
        #
        # Open a list for final results
        #
        final = []
        for num in nums:
            #
            # Split each ambig into tokens
            #
            toks = num.split()
            #
            # Open a return list for finalized items
            #
            fin = []
            #
            # Process tokens in reverse order, protecting against
            # leading and trailing comma cruft.
            #
            toks.reverse()
            pos = -1
            for tok in toks:
                tok = tok.strip(',')
                pos += 1
                #
                # Check for an irregularly formed token.  Examples would 
                # be "2,23,300", or "945,2".  There is no way to tell
                # what the hell these mean, so we set them on the stack
                # for processing, as if the comma(s) weren't in there.
                # But if the OCR is this bad, we're probably going to
                # lose here.
                #
                if ',' in tok:
                    broken = False
                    for t in tok.split(',')[1:]:
                        if len(t) != 3:
                            print 'Bad token, attempting fix'
                            broken = True
                            break
                    if broken:
                        for t in tok.split(','):
                            toks.insert( pos+1, t )
                        continue
                #
                # There four things we can do if the working
                # list is currently empty.
                #
                if not self.wrk:
                    #
                    # [DONE]
                    # If a token contains at least one comma and ends
                    # in one or two numerals, it's an immediate wrap
                    #
                    if ',' in tok and len(tok.split(',')[0]) < 3:
                        fin.append(tok)
                        continue
                    # [DONE]
                    # If a token contains no comma and is not exactly
                    # three digits in length, it's an immediate wrap.
                    # This will pass through both crufty numbers like
                    # lone "1" or "2", and longer numbers, such as a
                    # year.  Most of these will fall out during
                    # validation.
                    #
                    if not ',' in tok and len(tok) != 3:
                        fin.append(tok)
                        continue
                    # [DONE]
                    # Otherwise, we must have one or more three-digit 
                    # strings separated by commas. Append this to the 
                    # working list.  (Hmm. Bad. This could be the
                    # end of the line.)
                    #
                    self.wrk.append( tok )
                    continue
                # [DONE]
                # Pick up any additional three-digit strings and add
                # them to the working list
                #
                tsplit = tok.split(',')
                isthree = True
                for t in tsplit:
                    if not len(t) == 3:
                        isthree = False
                if isthree:
                    self.wrk.append( tok )
                    continue
                # [DONE] (implicitly handled by singleton test in new code)
                # If the current token is a single "0", finalize the
                # working list and the 0.
                #
                if tok == "0":
                    fin.append( self.combine_tokens() )
                    fin.append( tok )
                    continue
                #
                # When get get here, we have a regular set of tokens on the working
                # list, and a string of 1-2 digits in the current token.  Attempt
                # to find a split point.
                #
                if len(tok) < 3:
                    #
                    # Our fragmentary token must be merged with the
                    # last token on the working list, it cannot stand
                    # alone.
                    #
                    self.wrk[-1] = tok + ',' + self.wrk[-1]
                    fin.append( self.combine_tokens() )
            #
            # If we reach here with something on the working list,
            # we have to figure out what to do with it.
            #
            if self.wrk:
                fin.append( self.combine_tokens() )
            #
            # Add confirmed items to final list
            #
            fin.reverse()
            final.append(fin)
        
        #
        # Tuples embedded in the list indicate ambiguities.
        # It's now time for brute force.  We generate a 
        # page for every possible combination.
        #
        ## final[4].append( ('123 456,789', '123,456 789', '123,456,789') )
        #
        seed = []
        for fpos in range(0,len(final),1):
            line = final[fpos]
            for lpos in range(0,len(line),1):
                item = line[lpos]
                if type(item) == type( (1,) ):
                    seed.append( (fpos,lpos,0) )
        
        #
        # For every cluster of ambiguities, we generate a resolution set for
        # each of its possibilities. Each set goes on the list
        # of known combinations, and must be processed for every
        # succeeding cluster.  The combinations list will grow
        # very fast.  Theoretically, this could consume all of the
        # memory in the machine.  Is this fun, or what?
        #
        combinations = [seed]
        for spos in range(0,len(seed),1):
            if self.i_give_up: break
            addr = seed[spos]
            ambiguities = final[ addr[0] ][ addr[1] ]
            for apos in range(1,len(ambiguities),1):
                if self.i_give_up: break
                #
                # In reverse order, so that adding to the list of
                # cominations will not affect the current pass.
                #
                for cpos in range(len(combinations)-1,-1,-1):
                    combination = copy.deepcopy(combinations[cpos])
                    #
                    # A fixed combination is an address, plus one
                    # of the possibilities from the tuple registered
                    # in final. 
                    #
                    combination[spos] = (addr[0], addr[1], apos)
                    #
                    # Python to the rescue.  Comparing entire lists
                    # of tuples for equality to avoid duplication.
                    #
                    if len(combinations) > 500:
                        self.i_give_up = True
                        break
                    if not combination in combinations:
                        combinations.append(combination)
        #
        # print 'The list of all possible combinations!'
        #
        finals = []
        for combination in combinations:
            finalfinal = copy.deepcopy(final)
            for c in combination:
                finalfinal[ c[0] ][ c[1] ] = final[ c[0] ][ c[1] ][ c[2] ]
            finals.append(finalfinal)
        
        texts = []
        for final in finals:
            mytxt = copy.deepcopy(txt)
            for pos in range(len(mytxt)-1,-1,-1):
                mytxt.insert( pos, ' '.join(final[pos-1]) )
        
            mytxt = ''.join( mytxt )
        
            texts.append( mytxt )
        return texts
        
class Assumption:
    
    def __init__(self, dumb_ideas ):
        self.dumb_ideas = dumb_ideas
        self.i_am_done = False
        
    def test(self, itemp, check_totals=False ):
        myval = self.dumb_ideas[ itemp ][2]
        
        if myval > 0 and myval >= self.dumb_ideas[ itemp-1 ][2]:
            #
            # Ask to give up, return false
            if self.total( itemp, check_totals=check_totals ) < myval:
                return -1
            #
            # Report good total
            elif self.total( itemp, check_totals=check_totals ) == myval:
                return 0
            #
            # Ask to try again
            else:
                return 1
        else:
            #
            # If there is no point, ask to give up
            return -1

    def total(self, itemp, check_totals=False):
        # XXX
        elements = []
        for pos in range(itemp-1,-1,-1):
            if check_totals:
                if self.dumb_ideas[pos][0] == 'total':
                    elements.append( self.dumb_ideas[pos][2] )
            else:
                if self.dumb_ideas[pos][0] == 'total':
                    break
                elif self.dumb_ideas[pos][0] == 'element':
                    elements.append( self.dumb_ideas[pos][2] )
        return sum( elements )
        
    def totals(self):
        totals = []
        for pos in range(len(self.dumb_ideas)-1,-1,-1):
            idea = self.dumb_ideas[pos]
            if idea[0] == 'total':
                totals.append(pos)
        return totals

    def maketotal(self, itemp, check_totals=False):
        if check_totals:
            self.dumb_ideas[itemp][0] = 'total_grand'
            self.i_am_done = True
        else:
            self.dumb_ideas[itemp][0] = 'total'

    def identity(self):
        #
        # Report my tagging pattern as far as we have progressed.
        # Used to determine whether this same set of
        # assumptions is already on the assumptions list.
        return ','.join( [x[0] for x in self.dumb_ideas] )

    def unwind(self, totalp):
        newself = copy.deepcopy( self )
        #
        # find a previous total, if any
        topofsection = 0
        for pos in range(totalp,-1,-1):
            if newself.dumb_ideas[pos][0] == 'total':
                topofsection = pos+1
                break
        for pos in range(topofsection, len(self.dumb_ideas), 1):
            newself.dumb_ideas[pos][0] = 'element'
        return newself
    
    def encruft(self, itemp, check_totals=False):
        #
        # Mark the smallest item in the qualifying range
        # as cruft.  Return False if nothing left to work with.
        candidates = []
        for pos in range(itemp-1,-1,-1):
            idea = self.dumb_ideas[pos]
            if check_totals:
                if idea[0] == 'total':
                    candidates.append( (pos, idea[2]) )
            else:
                if idea[0] == 'total':
                    break
                elif idea[0] == 'element':
                    candidates.append( (pos, idea[2]) )
        if candidates:
            candidates.sort( self.cruftsort )
            if check_totals:
                self.dumb_ideas[ candidates[0][0] ][0] = 'total_cruft'
            else:
                self.dumb_ideas[ candidates[0][0] ][0] = 'cruft'
            return True
        else:
            return False
        
    def overcruft(self):
        ''' Mark all entries in the scope of a total_cruft marker
            as cruft.
        '''
        label_cruft = False
        for pos in range(len(self.dumb_ideas)-1,-1,-1):
            idea = self.dumb_ideas[pos]
            if idea[0] == 'total':
                label_cruft = False
            if label_cruft:
                self.dumb_ideas[pos][0] = 'cruft'
            if idea[0] == 'total_cruft':
                label_cruft = True

    def decruft(self, itemp, check_totals=False):
        ''' Reverse the effects of encruft
        '''
        for pos in range(itemp-1,-1,-1):
            idea = self.dumb_ideas[pos]
            if check_totals:
                if idea[0].startswith('total'):
                    self.dumb_ideas[pos][0] = 'total'
            else:
                if idea[0].startswith('total'):
                    break
                else:
                    self.dumb_ideas[pos][0] = 'element'
        
    def cruftsort(self, a, b):
        if a[1] > b[1]:
            return 1
        elif a[1] == b[1]:
            return 0
        else:
            return -1
        
    def dump(self):
        self.overcruft()
        obj = []
        elements = []
        if not self.total_grand():
            return (obj,0,'quality-flag')
        for idea in self.dumb_ideas:
            if idea[0] == 'element':
                elements.append( (idea[1],idea[2]) )
            elif idea[0] == 'total':
                obj.append( (elements[:],idea[2]) )
                elements = []
        return (obj,self.total_grand(),'quality-flag')
    
    def total_grand(self):
        for pos in range(len(self.dumb_ideas)-1,-1,-1):
            if self.dumb_ideas[pos][0] == 'total_grand':
                return self.dumb_ideas[pos][2]
        return 0
    
    def best_total_pos(self):
        for pos in range(len(self.dumb_ideas)-1,-1,-1):
            if self.dumb_ideas[pos][0] == 'total':
                return pos
        return -1

class Assumptions:
    
    def __init__(self):
        self.assumptions = []
        self.data = None
        self.got_grand_total = False

    def spill(self):
        for idea in self.assumptions[0].dumb_ideas:
            print '%10s %4s %s' % (idea[0],idea[1],idea[2])
        
    def ponder(self):
        #
        # Pasta, anyone?
        #
        
        #
        # The number of dumb_ideas never changes,
        # but we come up with fresh assumptions
        for itemp in range(0,len(self.assumptions[0].dumb_ideas),1):
            for assumptionp in range(len(self.assumptions)-1,-1,-1):
                assumption = self.assumptions[ assumptionp ]
                if assumption.i_am_done:
                    continue
                #
                # Test an assumption
                result = assumption.test( itemp )
                if result == 0:
                    assumption.maketotal( itemp )
                elif result == 1:
                    # If the assumption might be polluted by cruft, try that out
                    result = 1000
                    while assumption.encruft( itemp ):
                        result = assumption.test( itemp )
                        if result == 0:
                            assumption.maketotal( itemp )
                            break
                    if result != 0:
                        assumption.decruft( itemp )
                    totalitems = assumption.totals()
                    for totalitem in totalitems:
                        freshassumption = assumption.unwind( totalitem )
                        result = freshassumption.test( itemp )
                        if result == 0:
                            freshassumption.maketotal( itemp )
                            if not freshassumption.identity() in [x.identity() for x in self.assumptions]:
                                self.assumptions.append( freshassumption )
                else:
                    #
                    # If the assumption was hopeless, check if it works out to a grand total
                    result = assumption.test( itemp, check_totals=True )
                    if result == 0:
                        assumption.maketotal( itemp, check_totals=True )
                        self.got_grand_total = True
                    elif result == 1:
                        result = 1000
                        while assumption.encruft( itemp, check_totals=True ):
                            result = assumption.test( itemp, check_totals=True )
                            if result == 0:
                                assumption.maketotal( itemp, check_totals=True)
                                self.got_grand_total = True
                                break
                        if result != 0:
                            assumption.decruft( itemp, check_totals=True )
            if self.got_grand_total:
                break
        best_pos = 0
        best_total_pos = 0
        for pos in range(0,len(self.assumptions),1):
            if self.assumptions[pos].best_total_pos() > best_total_pos:
                best_total_pos = self.assumptions[pos].best_total_pos()
                best_pos = pos
        self.data = self.assumptions[pos].dump()
        return self.data
    
    def report(self):
        for category in self.data[0]:
            for line in category[0]:
                print '%-12s %9d' % (line[0],line[1])
            print '%22s' % ('---------',)
            print '%-12s %9d\n' % ('Total:',category[1])
        print '%22s' % ('---------',)
        print '%-12s %9d' % ('Grand total:',self.data[1])

    def load(self, txt ):
        result = re.findall( rstring, txt )
        #
        # Find start position
        start = -1
        for pos in range(0,len(result),1):
            if re.match(rSstring,result[pos]):
                start = pos
                break
        if start == -1:
            print 'no start found'
            #sys.exit()
            start = 0
        #
        # Find end position (needs some refinement)
        #
        # We also need to cope with the possibility of missing
        # commas.  Unpaper sometimes rips these out, and some
        # statements have no commas between digits in the first
        # place.  To handle these, we need 
        #
        end = -1
        for pos in range(0,len(result),1):
            if re.match(rEstring,result[pos]):
                end = pos
                break
        if end == -1:
            #print 'no explicit end found'
            end = len(result)
        #
        # Narrow to area of interest
        result = result[start:end]
        #
        # Build structured list
        dumb_ideas = []
        category = 'Unknown'
        for item in result:
            isnumber = re.match( rnumber, item )
            if isnumber:
                number = int( isnumber.group(1).replace(',','') )
                dumb_ideas.append(['element',category,number])
            else:
                for pos in range(0,len(categoryflags),1):
                    flags = categoryflags[pos]
                    if item in flags:
                        category = categoryname[pos]
                        break
        assumption = Assumption( dumb_ideas )
        self.assumptions.append( assumption )

if __name__ == '__main__':

    #d = disAmbiguate()
    #print dir(d)
    #sys.exit()
    
    txt = '''2006年度特定非営利活動に係る事業会計収支計算書
2006年4月 1 日から2007年3月 31 日まで
特定非営利活動5ま人 日 事】 《一・）十ル方5一構会
科 目 額 (単位 円）
（> 収 の,)
1経常収入の部
1会費収入
年会賃( 1団人・5ま人） 1,360,000
費助会賃(借人・賃五人) 0
書講定講日市 495,000 1,855,000
2事業収入
講講構定事業収入 11,182,000
補業位活動事業収入 0
講費・町開事業収入 1,185,000
町借・講座・講講事業収入 2,107,468
座講事業収入 288,660
受の地 収入 0 14,763,128
3講ま金道開収入
講取金利息収入 964 964
経常収入合計 16,619,092
0経常支出の部
1事業費
位講構定事業費 6,277,297
補業ま活動事業費 0
  2,727,102
町借・講座・講） 業費 222,910
座事度事業費 1,411,805
での地 費 0 10,639,114
2費費費
人特費 834,500
賃借料 970,000
借品費 0
道1書費 302,243
事講5常事講品費 525,270
販費支道費 184,430
和講公講 0
補会費 11,500
書 商費 40,000
  17,654
講特支構費 25,500
支払手額料 22,120
雑費 , 58,922 2,992,139
経常支出合計 13,631,253
経常収支書額 2,987,839
当期収支費額 2,987,839
補期構講収 額 4,682,882
家期寄業講収 額 7,670,721
（年開助商ま費道の部)
町年構助商借加の部
1貸度構加額
当期収支書額 2,987,839
2賃億5成公額
構加額合計 0 2,987,839 2,987,839
村年町助費道機の部
1賃商補出額
当期収支書額 0
2賃億構加額
5成金額合計 0 0 0
当期年特助 日加額（動公額) 2,987,839
補期経講町ま助構額 4,682,882
当期年特助度合計 7,670,721
'''.decode('utf8')
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--orig':
            print txt
            sys.exit()
        else:
            ifh = open( sys.argv[1] )
            ifh.readline()
            ifh.readline()
            ifh.readline()
            txt = ifh.read().decode('utf8','replace')

    disambiguator = disAmbiguate()
    texts = disambiguator.disambiguate( txt )
    for text in texts:
        sys.stdout.write('.')
        sys.stdout.flush()
        thinker = Assumptions()
        thinker.load( text )
        thinker.ponder()
        if not thinker.got_grand_total:
            continue
        print '\n================'
        print 'Confirmed values'
        print '================'
        thinker.report()
        #thinker.spill()
        sys.exit()
    print '\nNo total found'

#if __name__ == '__main__':
#    txt = open('sample1.txt').read()
#    disambiguator = disAmbiguate()
#    texts = disambiguator.disambiguate( txt )
#    for text in texts:
#        print text

