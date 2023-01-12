import { get } from "../../../common/apiHelper"
import { DONWLOAD_ENDPOINT } from "../../../constants"

export const download = (password: string, id: string) => get(`${DONWLOAD_ENDPOINT}/${id}`, {
    'Authorization': password
})