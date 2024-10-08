'use client'
import { AppContext } from "@/Contexts/AppContext"
import { Category } from "@/utils/Types"
import { useContext, useEffect } from "react"
// const getCategories = async ()=>{
//     const categories =  await fetch('http://localhost:8000/api/categories/')
//     return categories.json()
// }




export default function Categories(){
    const {categories,setCategories} = useContext(AppContext)
    const getCategories = async ()=>{
        if(categories == undefined){
        try{
            const response = await fetch('http://localhost:8000/api/categories/')
            if(response.ok){
                const data = await response.json()
                setCategories(data)
                console.log(data)
            }
        }catch(error){
            console.log(error)
        }
        
    }

    }


    useEffect(()=>{
        getCategories()
    },[])

    return (
        <div>
        <>
            { categories &&
                (categories.map((category:Category )=>{
                    return(
                    <div key={category.id}>
                    <h2 key={category.id} className="hover:text-[#E73F10]">{category.name}</h2>
                    {category.children &&
                        category.children.map((subcat:Category)=>{
                         return <h2 key={subcat.id} className="ml-2 hover:text-[#E73F10]" > - {subcat.name}</h2>
                        })
                    }
                    
                    </div>
                    )
                })
                )
        }
        </>
        </div>
    )
}