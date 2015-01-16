
import pprint
import sys
from datetime import date

class Customer:

	
	customer_id = None
	playlists = None

	def __init__(self, customer_id):

		self.customer_id = customer_id
		self.playlists = {}


	def add_to_plays(self,  pl_name,  track_name, track_artist, duration):

		if pl_name in self.playlists:
			self.playlists[pl_name].append((duration, track_name, track_artist))			
		else:
			self.playlists[pl_name] = [(duration,  track_name, track_artist)]
			
		
	
	def print_pl(self):

		pprint.pprint(self.playlists)

	def get_most_played_playlist(self):
		"""returns a string with the playlist name"""

		pl = [(len(self.playlists[playlist]), playlist) for playlist in self.playlists ]			
		pl.sort()
		return pl[-1][1]

	def get_most_played_track_from_playlist(self, most_played_playlist):
		"""returns a tuple with the most played track in the playlist (duration, track_name, artist)"""

		return max(self.playlists[most_played_playlist])


customer_map = {}


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
		for customer in customer_map:
			row = []			
			row.append(customer)
			cust_instance = customer_map[customer]
			rec_playlist_name  = cust_instance.get_most_played_playlist()
			row.append(rec_playlist_name)
			dur, most_played_track_name, most_played_track_artist = cust_instance.get_most_played_track_from_playlist(rec_playlist_name )
			row.append(most_played_track_name)
			row.append(most_played_track_artist + '\n')
			f.writelines('\t'.join(row))
			customer_cnt += 1
	print('>>>output file {0} is ready with the playlist recommendations'.format(output_file))
	print(str(customer_cnt) + ' customers got a playlist recommendation')			

def process_line(line):

	customer_id, pl_asin, pl_name, track_asin, track_name, track_artist, duration = line.split('\t')
	
	duration = clean_duration(duration)
	if customer_id not in customer_map:
		customer_map[customer_id] = Customer(customer_id)
		customer_map[customer_id].add_to_plays(pl_name, track_name, track_artist, duration)		
	else:
		customer_map[customer_id].add_to_plays(pl_name, track_name, track_artist, duration)

def clean_duration(duration):
	duration = duration.strip()
	if duration.isdigit(): 
		duration = float(duration)
	else:
		duration = 0
	return duration

def main():

	wild_card_date = str(date.today())
	data_file = sys.argv[1]
	read_data(data_file)
	write_out(data_file.split('.')[0] + '_output_' + wild_card_date + '.tsv')

		

main()
	


