
# -*- coding: latin-1 -*-
import bsddb
import pprint
import sys
from datetime import date
import json 






def add_to_plays( pl_name,  track_name, track_artist, duration, pl ):

	
	if pl_name in pl:
		pl[pl_name].append((duration, track_name, track_artist))			
	else:
		pl[pl_name] = [(duration,  track_name, track_artist)]
	
	return json.dumps(pl)
			
	

def clean_duration(duration):
	duration = duration.strip()
	if duration.isdigit(): 
		duration = float(duration)
	else:
		duration = 0
	return duration


def get_most_played_playlist(playlists):
	"""returns a string with the playlist name"""

	pl = [(len(playlists[playlist]), playlist) for playlist in playlists ]			
	pl.sort()
	return pl[-1][1]


def get_most_played_track_from_playlist( most_played_playlist):
	"""returns a tuple with the most played track in the playlist (duration, track_name, artist)"""
	l = [ (clean_duration(duration), track_name, artist)  for duration, track_name, artist in most_played_playlist ]
	return max(l)



def read_data(file_name):

	print('>>>reading data')
	with open(file_name, 'rU') as f:
		f.readline()
		for line in f:
			process_line(line)
					
	print('>>>finished reading data')


def write_out(output_file):

	print('>>>writing output')
	customer_cnt = 0 
	with open(output_file, 'w') as f:	
		for customer, playlists in customer_map.iteritems():
			row = []			
			row.append(customer)
			playlists = json.loads(playlists)
			rec_playlist_name  = get_most_played_playlist(playlists)
			row.append(rec_playlist_name.encode('utf-8'))
			tracks_from_rec_pl = playlists[rec_playlist_name]
			dur, most_played_track_name, most_played_track_artist = get_most_played_track_from_playlist(tracks_from_rec_pl)
			row.append(most_played_track_name.encode('utf-8'))
			row.append(most_played_track_artist.encode('utf-8') + '\n')
			#print(row)
			f.write('\t'.join(row))
			customer_cnt += 1
	print('>>>output file {0} is ready with the playlist recommendations'.format(output_file))
	print(str(customer_cnt) + ' customers got a playlist recommendation')			

def process_line(line):

	customer_id, pl_asin, pl_name, track_asin, track_name, track_artist, duration = line.split('\t')
	duration = duration.strip()
	if customer_map.has_key(customer_id):
		pl = json.loads(customer_map[customer_id])
		customer_map[customer_id] = add_to_plays(pl_name,  track_name, track_artist, duration, pl)		
	else:
		customer_map[customer_id] = add_to_plays(pl_name,  track_name, track_artist, duration, pl = {})



def clean_duration(duration):
	duration = duration.strip()
	if duration.isdigit(): 
		duration = float(duration)
	else:
		duration = 0
	return duration

customer_map = bsddb.btopen('customer_data.db' , 'c')

def main():

	wild_card_date = str(date.today())
	data_file = sys.argv[1]
	read_data(data_file)
	data_file = 'test_out_put.tsv'
	write_out(data_file.split('.')[0] + '_output_' + wild_card_date + '.tsv')

	#customer_map['B00PZHTSOM'].print_pl()

	

main()
	
