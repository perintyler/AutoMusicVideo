
import os
import pathlib
import storyboard

INPUT_AUDIO_DIRECTORY = 'input-audio'

def main():
  for audio_file in os.listdir(INPUT_AUDIO_DIRECTORY):
    song_path = pathlib.Path(INPUT_AUDIO_DIRECTORY).joinpath(audio_file)
    song_id = song_path.stem

    storyboard.write_table_of_contents(song_id, audio_file)
    
    for job in storyboard.generate_jobs(song_id):
      storyboard.do_job(song_id, job)

if __name__ == '__main__':
  main()
