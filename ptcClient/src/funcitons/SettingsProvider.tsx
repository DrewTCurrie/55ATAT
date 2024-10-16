import { createContext, ReactNode, useContext } from "react";

//Create element that can be read by the rest of the webapp
const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

//Interface to wrap components within the app.
interface settingsProps {
    children: ReactNode;
};

interface SettingsContextType {
    message: string,
    audioFile: File,
    setMessage: (message: string) => void,
    setAudio: (audioFile: File) => void,
    getMessage: (attendeeID: string) => string,
    getAudio: (attendeeID: string) => File,
    getDefaultMessage: () => string,
    getDefaultAudio: () => File
};

const SettingsProvider: React.FC<settingsProps> = ({children}) => {

    //Get Message, get Initials, get Audio
    //Set Defaults
    //Set Message for Initials

    const getDefaultMessage = () => {

    }
    const getDefaultAudio = () => {

    }
    const setAttendeeMessage = () => {

    }
    const setAttendeeAudio = () => {
        
    }

    return(
        <SettingsContext.Provider>

        </SettingsContext.Provider>
    );
};

export default SettingsProvider;

export const useSettings = () => {
    return useContext(SettingsContext);
}
