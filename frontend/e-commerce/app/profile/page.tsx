import UserDetails from "@/components/profile/UserDetails";




export default async function ProfilePage(){
    
    return(
        <div className="w-full h-screen flex justify-center">
            <div className="h-[60%] w-[50%] bg-gray-100 rounded-md">
                <UserDetails />

            </div>
        
        </div>
    )
}