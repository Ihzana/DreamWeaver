# cinematic_engine.py

class CinematicEngine:
    def create_storyboard(self, parsed_data: dict):
        print("Creating storyboard...")
        storyboard = []
        
        # Determine overall style based on emotion and symbols
        style_prompt = "cinematic, high detail, 8k"
        if parsed_data['dominant_emotion'] == 'negative' or parsed_data['symbols_actions'].get('anxiety', 0) > 0.7:
            style_prompt += ", film noir, dark, high contrast, dramatic shadows"
        elif parsed_data['symbols_actions'].get('freedom', 0) > 0.7 or parsed_data['symbols_actions'].get('flying', 0) > 0.7:
             style_prompt += ", surrealist, vibrant colors, wide angle lens, Ghibli-esque"
        else:
            style_prompt += ", indie drama, soft focus, natural lighting"
            
        # Create shots from sentences
        sentences = re.split(r'(?<=[.!?]) +', parsed_data['original_text'])
        shot_duration = 3 # seconds per shot

        for i, sentence in enumerate(sentences):
            prompt = f"{sentence.strip()}, {style_prompt}"
            camera_motion = "static"
            
            # Add camera motion based on content
            if "running" in sentence or "chase" in sentence:
                camera_motion = "shaky cam, fast tracking shot"
            if "flying" in sentence:
                camera_motion = "slow majestic dolly shot, aerial view"
            if "falling" in sentence:
                camera_motion = "dizzying top-down shot, fast zoom in"
            
            shot = {
                "shot_number": i + 1,
                "prompt": prompt,
                "camera_motion": camera_motion,
                "duration": shot_duration,
                "emotion": parsed_data['emotional_arc'][i] if i < len(parsed_data['emotional_arc']) else 'NEUTRAL'
            }
            storyboard.append(shot)
            
        print("...Storyboard complete.")
        return storyboard, parsed_data['dominant_emotion']