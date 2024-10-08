'use client'

import { fetchWithAuth } from "@/utils/Helpers"
import { UserInfos } from "@/utils/Types"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"



export default function UserDetails(){
    const [userDetails,setUserDetails] = useState<UserInfos>()
    const [error,setError] = useState<string>()
    const [isLoading,setIsLoading] = useState<Boolean>(false)
    const router = useRouter()

    useEffect(()=>{
        const access = localStorage.getItem('access')
        if(!access){
            router.push('/login')
        }
    },[])
    useEffect(()=>{
        const getUserInfos = async ()=>{
                try {
                    setIsLoading(true)
                    const response = await fetchWithAuth('http://localhost:8000/api/auth/users/me/')
                    if(!response.ok){
                        throw new Error('something went wrong!')
                    }
                    const data = await response.json()
                    console.log('user data: ',data)
                    setUserDetails(data)
                    setIsLoading(false)
                    
            }catch(e){
                const error = e as Error
                setIsLoading(false)
                 setError(error.message)
            }
                }
        getUserInfos()
    },[])

    return (
        <div className="w-full h-full flex justify-center">
            {isLoading &&
            <div className="w-full h-full flex justify-center items-center">
                <p>Loading...</p>
            </div>
            }
            {error &&
            <div className="w-full h-full flex justify-center items-center">
                <p>{error}</p>
            </div>
            }
            {userDetails &&
            <div className="w-full h-full flex flex-col items-center gap-4 mt-8" >
                <Image className="rounded-full" src={'/user.jpg'} width={200} height={200} alt="user profile picture" />
                {userDetails.first_name &&
                <div className="flex gap-4 bg-gray-400 px-4 py-2">
                    <p className="text-2xl font-semibold text-white">First name:</p>
                    <p className="text-2xl font-semibold text-[#E73F10]">{userDetails.first_name}</p>
                </div>}
                {userDetails.last_name &&
                <div className="flex gap-4 bg-gray-400 px-4 py-2">
                    <p className="text-2xl font-semibold text-white">Last name:</p>
                    <p className="text-2xl font-semibold text-[#E73F10]">{userDetails.last_name}</p>
                </div>}
                <div className="flex gap-4 bg-gray-400 px-4 py-2">
                    <p className="text-2xl font-semibold text-white">Email:</p>
                    <p className="text-2xl font-semibold text-[#E73F10]">{userDetails.email}</p>
                </div>
            </div>
            }

        </div>
    )
}