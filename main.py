"""main.py"""

from lyrics import Lyrics

COMPILE_VIDEO_WHEN_COMPLETE = False

def main(path_to_song, song_name):
  song_id = '-'.join(song_name.split(' '))
  segments_json_file = os.path.join(song_id, f'segments.json')
  multimedia_directory = os.path.join(song_id, 'multimedia')

  for directory in (song_id, multimedia_directory):
    if not os.path.isdir(directory):
      os.mkdir(directory)

  if os.path.exists(segments_json_file):
    music_video = MusicVideo.load_from_json(segments_json_file)
  else:
    music_video = MusicVideo.create_new(path_to_song)
    music_video.save_as_json(segments_json_file)

    if input(f'A segments file has been created at {segments_json_file}.'
          + 'Do you want to check that the lyrics were transcribed correctly '
          + 'before generating images? (y/n)'
    ) == 'y': return


  while not music_video.is_complete():
    segment = next(music_video.generate_incomplete_segments())
    line_number = segment.bar.line_number
    path_to_gif = os.path.join(multimedia_directory, f'{line_number}.json')
    generate_gif(bar, path_to_gif)
    music_video.set_multimedia(line_number, path_to_gif)
    music_video.save_as_json(segments_json_file)

  if input(f'All multimedia for the video has been successfully generated.'
        + 'Are you ready to compile and save the final video? (y/n)'
  ) != 'y': return

  path_to_music_video = os.path.join(song_id, 'music-video.mp4')
  music_video.compile(path_to_music_video)

if __name__ == '__main__':
  main()