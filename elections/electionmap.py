# n.races[0].reporting_units[0].results
from decimal import Decimal, ROUND_DOWN
from elections.ap import AP, Race
from elections.settings import FTP_USER, FTP_PASSWORD, MAP_RESULTS_DEST
from dateutil.parser import parse as dateparse
import os
try:
    import json
except ImportError:
    import simplejson as json

colors = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', 
'#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F', '#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', 
'#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F','#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', 
'#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F','#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', 
'#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F','#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', 
'#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F',]
legend_tmpl = "<tr><td style='width=32px;background-color:%(color)s'>&nbsp;</td><td>%(name)s</td><td>%(vote_total)s</td><td>%(vote_percent)#.2f%%</td></tr>"


def parse_race(race):
    """
    Loop through the reporting units and return a dict for output
    """
    county_results = {} # key = county number
    county_winners = {} # key = county number, 
    candidate_colors = {}
    legend = ['<table id="legendtable">']
    candidates = []
    total_votes = 0
    
    for i, cand in enumerate(race.candidates):
        cand_vote_total = getattr(cand, 'vote_total', 0)
        total_votes += cand_vote_total
        candidate_colors[cand.ap_natl_number] = colors[i]
        candidates.append({
            'name': cand.name, 
            'color': colors[i], 
            'vote_total': cand_vote_total, 
            'vote_percent': 0, 
            'delegates': cand.delegates,
        })
    candidate_colors['No winner'] = "#999"
    candidates.sort(key=lambda x: x['vote_total'], reverse=True)
    for cand in candidates:
        if total_votes:
            cand['vote_percent'] = round(cand['vote_total']/float(total_votes) * 100, 1) 
        else:
            cand['vote_percent'] = 0.0
        legend.append(legend_tmpl % cand)
    legend.append('</table>')
    
    for county in race.counties:
        winning_votes = 0
        if county.precincts_reporting_percent:
            precincts_reporting_percent = str(Decimal(str(county.precincts_reporting_percent)).quantize(
                                                        Decimal('.1'), rounding=ROUND_DOWN))
        else:
            precincts_reporting_percent = '0.0'
        
        county_results[county.fips] = {
            "name": county.name,
            "precincts_reporting": county.precincts_reporting,
            "precincts_reporting_percent": precincts_reporting_percent,
            "precincts_total": county.precincts_total,
            "results": []
        }
        for result in county.results:
            if result.vote_total is None:
                vote_total = 0
            else:
                vote_total = result.vote_total
            if result.vote_total_percent is None:
                vote_total_percent = 0.0
            else:
                vote_total_percent = str(Decimal(str(result.vote_total_percent)).quantize(
                                                        Decimal('.1'), rounding=ROUND_DOWN))
                
            county_results[county.fips]['results'].append({
                "ap_natl_number": result.candidate.ap_natl_number,
                "name": result.candidate.name,
                "vote_total": vote_total,
                "vote_total_percent": vote_total_percent,
            })
            if vote_total > winning_votes:
                winning_votes = vote_total
                county_winners[county.fips] = result.candidate.ap_natl_number
            elif vote_total == winning_votes:
                county_winners[county.fips] = 'No winner'
        county_results[county.fips]['results'].sort(key=lambda x: x['vote_total'], reverse=True)
    
    return {
        "candidate_colors": candidate_colors, 
        "legend": "".join(legend),
        "county_results": county_results,
        "county_winners": county_winners
    }

def write_results(electiondate, path_to_data=None, path_to_inits=None):
    # Use county_winners to color states using candidate_colors
    client = AP(FTP_USER, FTP_PASSWORD)
    
    # If the paths are send in the paths specifif top of ticket
    if path_to_data and path_to_inits:
        n = client.get_topofticket_paths_specified(electiondate, path_to_data, 
                                                   path_to_inits)
    else:
        # else use default
        n = client.get_topofticket(electiondate)
    
    dt = dateparse(electiondate)
    directory = os.path.join(MAP_RESULTS_DEST, str(dt.year))
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Detail county results
    for race in n.races:
        # Gracefully handle no state or party being empty
        if not race.state:
            continue
    
        results = parse_race(race)
        
        # Next block is trying to create detailed file name this is usuable as a file
        state = race.state.abbrev
        if race.race_type in Race._race_types:
            race_type = Race._race_types[race.race_type][:7]
        else:
            race_type = race.race_type
        office_name = race.office_name.replace('.', '').replace(' ', '_')
        
        # This is for amendments mostly since ammendments have / in them
        seat_name = race.seat_name.replace('/', '-').replace(' ', '_').replace('_-_', '-')
        file_name = "%s-%s-%s-%s" %(electiondate, state, race_type, office_name)
        if seat_name:
            file_name = "%s-%s" % (file_name, seat_name)
        file_name = '%s.json' % file_name
        f = open(os.path.join(directory, file_name), "w")
        f.write(json.dumps(results))
        f.close()