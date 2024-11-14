import React, { useEffect } from "react";
import './audioPlayer.css'


interface AudioPlayerProps {
    audioUrl: string | null,
    audioType: string | null, 
    autoPlay?: boolean | null,
    audioRef: React.RefObject<HTMLAudioElement> 
}

//This is so the audio player can reload, by adding a custom useEffect that activates when audioURL is changed.
export const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioUrl,audioType,autoPlay,audioRef }) => {
    useEffect(() => {
      // Reload the audio when the audioUrl changes
      if (audioRef.current) {
        audioRef.current.load();
        audioRef.current.currentTime = 0;
      }
    }, [audioUrl, autoPlay]);
  
    return (
      <div>
        <audio ref={audioRef} controls className={autoPlay ? 'hidden' : ''}>
          <source src={audioUrl || ''} type={audioType || ''} />
          Your browser does not support the audio element.
        </audio>
      </div>
    );
  };