# main.py
from dream_scribe import DreamScribe
from cinematic_engine import CinematicEngine
from generative_core import GenerativeCore
from film_assembler import assemble_film

def dream_to_movie(dream_text: str):
    """
    Main pipeline for the Oneiro AI.
    """
    print("--- ONEIRO AI: DREAM-TO-MINI-MOVIE SEQUENCE INITIATED ---")
    
    # 1. Parse the dream
    scribe = DreamScribe()
    parsed_dream = scribe.parse_dream_text(dream_text)
    print("\nPARSED DATA:")
    print(parsed_dream)
    
    # 2. Create a storyboard
    director = CinematicEngine()
    storyboard, dominant_emotion = director.create_storyboard(parsed_dream)
    print("\nSTORYBOARD:")
    for shot in storyboard:
        print(f"  - Shot {shot['shot_number']}: {shot['prompt']}")

    # 3. Generate the assets
    generator = GenerativeCore()
    total_duration = sum(s['duration'] for s in storyboard)
    
    print("\nGENERATING ASSETS:")
    video_clip_files = []
    for shot in storyboard:
        clip_file = generator.generate_video_clip(shot)
        video_clip_files.append(clip_file)
        
    audio_track_file = generator.generate_audio_track(dominant_emotion, total_duration)
    
    # 4. Assemble the final film
    print("\nFINAL ASSEMBLY:")
    output_filename = "MyDreamFilm.mp4"
    assemble_film(video_clip_files, audio_track_file, output_filename)
    
    print(f"\n--- SEQUENCE COMPLETE. Your Dream-Film is at '{output_filename}' ---")


if __name__ == "__main__":
    # The sample dream from the concept
    sample_dream = """
    I was running late for a flight. My legs felt like they were stuck in honey. 
    I was at the airport, but it was also a library, with giant, towering shelves of books. 
    I couldn't find my passport, and I kept pulling random objects out of my bag - a fish, a lit candle, a toy car. 
    I could hear the final boarding call for a place I've never heard of... 'Now boarding for Xylos'.
    """
    
    dream_to_movie(sample_dream)