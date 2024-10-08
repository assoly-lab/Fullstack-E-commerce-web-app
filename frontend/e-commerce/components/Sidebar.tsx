import { AppContext } from "@/Contexts/AppContext";
import { useContext } from "react";
import { IoCloseOutline } from "react-icons/io5";
import Categories from "./Categories";




export default function Sidebar(){
    const { isSidebar,setIsSidebar } = useContext(AppContext)

    return ( 
        <div className="fixed top-0 left-0 bg-[#E73F10]/30 w-full min-h-full z-40" onClick={ ()=>{
            setIsSidebar(!isSidebar)
        }}>
            <div className="w-[70%] h-screen bg-white fixed top-0 left-0 z-50" onClick={(e)=>{
                e.stopPropagation()
            }}>
                {/* scrollable div */}
                <div className="flex justify-between items-center border border-b-[#E73F10] ">
                    <h1 className="text-3xl pt-6 pl-4 uppercase">E-<span className="text-[#E73F10] ">Store</span></h1>
                    <IoCloseOutline className="w-[40px] h-[40px] mt-8 mr-2 cursor-pointer hover:text-[#E73F10]" onClick={()=>{
                        setIsSidebar(!isSidebar)
                    }
                    } />
                </div>
                {/* end of scrollable div */}
                <div className="pl-4 pt-4 pb-4 max-h-[calc(100vh-_73.6px)]  overflow-y-scroll">
                    <Categories />
                </div>
            </div>
        </div>

    )
}