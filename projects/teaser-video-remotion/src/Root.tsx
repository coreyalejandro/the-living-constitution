import React from 'react';
import { Composition } from 'remotion';
import { MainScene } from './scenes/MainScene'; // Your Boondocks Hustler
import { OldSchoolScene } from './scenes/OldSchoolScene'; // The original flat video
import { KimiScene } from './scenes/KimiScene'; // Placeholder for Kimi's version
import { VeoScene } from './scenes/VeoScene'; // Placeholder for Veo's version
import {
  VIDEO_DURATION_FRAMES,
  VIDEO_FPS,
  VIDEO_HEIGHT,
  VIDEO_WIDTH,
} from './composition/VideoConfig';

export const Root: React.FC = () => {
    return (
        <>
            {/* 1. THE LEAD: The Revolutionary Hustler (Boondocks Style) */}
            <Composition
                id="ImJustABuild"
                component={MainScene}
                durationInFrames={VIDEO_DURATION_FRAMES}
                fps={VIDEO_FPS}
                width={VIDEO_WIDTH}
                height={VIDEO_HEIGHT}
            />

            {/* 2. THE RETRO: The Original Flat Video (Preserved) */}
            <Composition
                id="OldSchoolBuild"
                component={OldSchoolScene}
                durationInFrames={300}
                fps={30}
                width={1080}
                height={1920}
            />

            {/* 3. THE KIMI: Porting Kimi's Cultural Nuance */}
            <Composition
                id="KimiRemix"
                component={KimiScene}
                durationInFrames={720}
                fps={12}
                width={1080}
                height={1080}
            />

            {/* 4. THE VEO: The Cinematic High-End Counterpart */}
            <Composition
                id="VeoCinematic"
                component={VeoScene}
                durationInFrames={144} // 6 seconds of high-end Veo footage
                fps={24}
                width={1280}
                height={720}
            />
        </>
    );
};
