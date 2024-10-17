import { createContext, ReactNode, useContext, useEffect, useState } from "react";
import * as React from 'react'

//Create element that can be read by the rest of the webapp
const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

//Interface to wrap components within the app.
interface settingsProps {
    children: ReactNode;
};

interface SettingsContextType {
    defaultMessage: string,
    attendeeMessage: string,
    //audioFile: File,
    setAttendeeMessage: (attendeeInitials: string, message: string) => void,
    getAttendeeMessage: (attendeInitials: string) => void,
    getDefaultMessage: () => void,
    setDefaultMessage: (message: string) => void,
    resetAttendee: (attendeInitials: string) => void,
    //setAudio: (attendeeID: string, audioFile: File) => void,
    //getAudio: (attendeeID: string) => File,
    //getDefaultAudio: () => File
    //setDefaultAudio: (audioFile: File) => void,
    resetDefaults: () => void,
    setDMessage: (message: string) => void,
    setAMessage: (message: string) => void,
};

const SettingsProvider: React.FC<settingsProps> = ({children}) => {

    //These two hooks are used to pass messages and editing across the Provider to other elements.    
    const [defaultMessage, setDMessage] = useState('')
    const [attendeeMessage, setAMessage] = useState('')

    /**
     * Fetching Functions
     */

    const [hasFetchedDmesg, setFetchedDmesg] = useState(false)
    useEffect(() => {
        if(!hasFetchedDmesg){
            getDefaultMessage();
        }  
    },[hasFetchedDmesg])

     /**
     * Attendee Message Functions
     */
    const getAttendeeMessage = async (attendeeInitials: string) => {
        const initials = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                initials: attendeeInitials
            })
        }
        try{
            const message = await fetch(`/api/getAttendeeMessage`,initials)
            const messageContent = await message.json()
            setAMessage(messageContent.message)
        } catch(e){
            console.log("Error Retrieving Default Message", e)
        }
    }

    const setAttendeeMessage = async (attendeeInitials: string, message: string) => {
        const attendeeMessage = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                initials: attendeeInitials,
                message: message
            })
        }
        try{
            const messageRespone = await fetch(`/api/setAttendeeMessage`,attendeeMessage)
            const messageResponeContent = await messageRespone.json()
        } catch(e){
            console.log("Error Changing Default Message", e)
        }
    }

    const resetAttendee = async (attendeeInitials: string) => {
        const attendee = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                initials: attendeeInitials,
            })
        }
        try{
            const resetRespone = await fetch(`/api/resetAttendee`, attendee)
            const resetResponeContent = await resetRespone.json()
            console.log(resetResponeContent)
            getAttendeeMessage(attendeeInitials)
        } catch(e){
            console.log("Error reseting Defaults", e)
        }
    }

    /*
    * Default Message Functions
    */
    
    const getDefaultMessage = async () => {
        try{
        const message = await fetch(`/api/getDefaultMessage`)
        const messageContent = await message.json()
        setDMessage(messageContent.message)
        setFetchedDmesg(true)
        } catch(e){
            console.log("Error Retrieving Default Message", e)
        }
    }

    const setDefaultMessage = async (message: string) => {
        const defaultMessage = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                message: message
            })
        }
        try{
            fetch(`/api/setDefaultMessage`,defaultMessage)
            setFetchedDmesg(false)
        } catch(e){
            console.log("Error Changing Default Message", e)
        }
    }

    const resetDefaults = async () => {
        try{
            fetch(`/api/resetDefaults`)
            setFetchedDmesg(false)
        } catch(e){
            console.log("Error reseting Defaults", e)
        }
    }
    return(
        <SettingsContext.Provider 
        value={{
            defaultMessage, 
            attendeeMessage, 
            getAttendeeMessage, 
            setAttendeeMessage, 
            resetAttendee,
            setAMessage, 
            setDMessage, 
            getDefaultMessage, 
            setDefaultMessage, 
            resetDefaults}}>
            {children}
        </SettingsContext.Provider>
    );
};

export default SettingsProvider;

export const useSettings = () => {
    return useContext(SettingsContext);
}
