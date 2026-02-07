import axios from "axios"
import {postconfig} from "@/common/request.js"

export const getList = () => axios.post("constants/ConstantsController/get_list", {}, postconfig())