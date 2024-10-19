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
    defaultAudio: string,
    attendeeAudio: string,
    setAttendeeMessage: (attendeeID: string, message: string) => void,
    getAttendeeMessage: (attendeeID: string) => void,
    getDefaultMessage: () => void,
    setDefaultMessage: (message: string) => void,
    resetAttendee: (attendeeID: string) => void,
    setAttendeeAudio: (attendeeID: string, audioFile: File) => Promise<void>,
    getAttendeeAudio: (attendeeID: string) => void,
    getDefaultAudio: () => void,
    setDefaultAudio: (audioFile: File) => void,
    getFailureAudio: () => void,
    resetDefaults: () => void,
    setDMessage: (message: string) => void,
    setAMessage: (message: string) => void,
    setDAudio: (audioURL: string) => void,
    setAAudio: (audioURL: string) => void,
};

const SettingsProvider: React.FC<settingsProps> = ({children}) => {

    //These two hooks are used to pass messages and editing across the Provider to other elements.    
    const [defaultMessage, setDMessage] = useState('')
    const [attendeeMessage, setAMessage] = useState('')
    const [defaultAudio, setDAudio] = useState('')
    const [attendeeAudio, setAAudio] = useState('')
    /**
     * Fetching Functions
     */

    const [hasFetchedDmesg, setFetchedDmesg] = useState(false)
    const [hasFetchedDAudio, setFetchedDAudio] = useState(false)
    useEffect(() => {
        if(!hasFetchedDmesg){
            getDefaultMessage();
        }
        if(!hasFetchedDAudio){
            getDefaultAudio();
        }  
    },[hasFetchedDmesg,hasFetchedDAudio])
    /**
     * Default Audio Functions
     */
    const getDefaultAudio = async () => {
        try{
            const audio = await fetch(`/api/getDefaultAudio`)
            const audioURL = await audio.json()
            setDAudio(audioURL.url)
            setFetchedDAudio(true)
            
        }catch(e){
            console.log("Error Retrieving Default Audio",e)
        }
        
    }
    const getFailureAudio = async () => {
        try{
            const audio = await fetch(`/api/getFailureAudio`)
            const audioURL = await audio.json()
            setAAudio(audioURL.url)
            setFetchedDAudio(true)
        }catch(e){
            console.log("Error Retrieving Default Audio",e)
        }
    }
    const setDefaultAudio = async (audioFile: File) => {
         const audio = new FormData();
         audio.append('audio', audioFile)
         const audioRequest = {
            method: 'POST',
            body: audio
         }
         try {
            const response = await fetch(`/api/setDefaultAudio`,audioRequest)
            if (!response.ok) {
                throw new Error('Error setting deafult audio');
            }
         }catch(e){
            console.log("Error setting default audio.",e)
         }
    }
    /**
     * Attendee Audio Functions
     */
    const getAttendeeAudio = async (attendeeID: string) => {
        const id = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                id: attendeeID
            })
        }
        try{
            const message = await fetch(`/api/getAttendeeAudio`,id)
            const messageContent = await message.json()
            setAAudio(messageContent.url)
        } catch(e){
            console.log("Error Retrieving Attendee Message", e)
        }
    }


    const setAttendeeAudio = async (attendeeID: string, audioFile: File) => {
        const audio = new FormData();
        audio.append('audio', audioFile)
        audio.append('id',attendeeID)
        const audioRequest = {
           method: 'POST',
           body: audio
        }
        try {
           const response = await fetch(`/api/setAttendeeAudio`,audioRequest)
           if (!response.ok) {
               throw new Error('Error setting Attendee audio');
           }
        }catch(e){
           console.log("Error setting Attendee audio.",e)
        }
   }

     /**
     * Attendee Message Functions
     */
    const getAttendeeMessage = async (attendeeID: string) => {
        const id = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                id: attendeeID
            })
        }
        try{
            const message = await fetch(`/api/getAttendeeMessage`,id)
            const messageContent = await message.json()
            setAMessage(messageContent.message)
        } catch(e){
            console.log("Error Retrieving Default Message", e)
        }
    }

    const setAttendeeMessage = async (attendeeID: string, message: string) => {
        const attendeeMessage = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                id: attendeeID,
                message: message
            })
        }
        try{
            await fetch(`/api/setAttendeeMessage`,attendeeMessage)
        } catch(e){
            console.log("Error Changing Default Message", e)
        }
    }

    const resetAttendee = async (attendeeID: string) => {
        const attendee = {
            method: 'POST',
            headers: {'Content-Type':'application/json',},
            body: JSON.stringify({
                id: attendeeID,
            })
        }
        try{
            const resetRespone = await fetch(`/api/resetAttendee`, attendee)
            const resetResponeContent = await resetRespone.json()
            console.log(resetResponeContent)
            getAttendeeMessage(attendeeID)
            getAttendeeAudio(attendeeID)
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
            defaultAudio,
            attendeeAudio,
            setAAudio,
            getAttendeeAudio,
            setAttendeeAudio,
            setAMessage,
            getAttendeeMessage, 
            setAttendeeMessage, 
            resetAttendee,
            setDAudio,
            getDefaultAudio,
            setDefaultAudio,
            getFailureAudio,
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
