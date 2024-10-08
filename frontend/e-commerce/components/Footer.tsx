import { FaAmazonPay, FaApplePay, FaBitcoin, FaCcVisa, FaFacebookF, FaInstagram, FaPaypal, FaTiktok, FaYoutube } from "react-icons/fa";
import { FaGooglePay, FaXTwitter } from "react-icons/fa6";
import { IoMdArrowDropdown } from "react-icons/io";



export default function Footer(){

    return (
        <div className="bg-[#EBEBEB] container">
            <div className="w-full pt-16 pl-4 mt-8 border border-b-gray-300 md:flex md:justify-center md:gap-24">
                <div className="w-[435px]">
                    <h3 className="font-medium text-2xl mb-6">About Us</h3>
                    <p className="mb-6">E-STORE is a dynamic and innovative online retail platform that offers a wide range of electronic products to customers worldwide.</p>
                    <div className="social-icons flex gap-4 mb-6">
                        <FaFacebookF className=" cursor-pointer hover:text-[#f98463]" />
                        <FaXTwitter className=" cursor-pointer hover:text-[#f98463]" />
                        <FaInstagram className=" cursor-pointer hover:text-[#f98463]" />
                        <FaYoutube className=" cursor-pointer hover:text-[#f98463]" />
                        <FaTiktok className=" cursor-pointer hover:text-[#f98463]" />
                    </div>
                    <h3 className="text-base font-medium mb-2">Guaranteed safe checkout</h3>
                    <div className="safe-checkout flex gap-2 [&>*]:hover:cursor-pointer mb-8">
                        <FaGooglePay className="h-8 w-12 bg-white px-1 py-1 rounded-md  hover:text-[#f98463]" />
                        <FaApplePay className="h-8 w-12 bg-white px-1 py-1 rounded-md hover:text-[#f98463]"  />
                        <FaAmazonPay className="h-8 w-12 bg-white px-1 py-1 rounded-md hover:text-[#f98463]"  />
                        <FaBitcoin className="h-8 w-12 bg-white px-1 py-1 rounded-md hover:text-[#f98463]"  />
                        <FaPaypal className="h-8 w-12 bg-white px-1 py-1 rounded-md hover:text-[#f98463]"  />
                        <FaCcVisa className="h-8 w-12 bg-white px-1 py-1 rounded-md hover:text-[#f98463]"  />
                    </div>
                </div>
                <DesktopLinks />
                <div className="links  pb-8 flex flex-col gap-6 md:aria-hidden md:hidden">
                    <div className="quick-links flex justify-between text-xl">
                        <p>Quick Links</p>
                        <IoMdArrowDropdown className="mt-2" />
                    </div>
                    <div className="informations flex justify-between text-xl">
                        <p>Informations</p>
                        <IoMdArrowDropdown className="mt-2"/>
                    </div>
                    <div className="policies flex justify-between text-xl">
                        <p>Policies</p>
                        <IoMdArrowDropdown className="mt-2"/>
                    </div>
                </div>
            </div>

            <div className="all-rights flex py-6 justify-center text-lg">
                <p>&copy; 2024 <span className="text-[#f98463]">E-</span>STORE, All rights reserved </p>
            </div>
            
        </div>
        ) 
}






const DesktopLinks = ()=>{
    return (
        <div className="container hidden md:flex md:gap-16 md:w-fit md:h-fit">
            <div className="links group">
                <p className="font-medium text-2xl mb-4 group-hover:text-[#f98463]">Quick Links</p>
                <p className="text-lg">My Account</p>
                <p className="text-lg">My Cart</p>
                <p className="text-lg">Need Help?</p>
            </div>
            <div className="links group">
                <p className="font-medium text-2xl mb-4 group-hover:text-[#f98463]">Informations</p>
                <p className="text-lg">About us</p>
                <p className="text-lg">Contact</p>
                <p className="text-lg">FAQ</p>
            </div>
            <div className="links group">
                <p className="font-medium text-2xl mb-4 group-hover:text-[#f98463]">Policies</p>
                <p className="text-lg">Privacy Policy</p>
                <p className="text-lg">Refund Policy</p>
                <p className="text-lg">Terms of Service</p>
            </div>
        </div>
    )
}