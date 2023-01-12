import { ContentType, get, post } from "../common/apiHelper";
import { INVALIDATE_UPLOAD_ENDPOINT, MAX_FILE_NAME_SIZE, UPLOAD_FILE_ENDPOINT, UPLOAD_START_ENDPOINT } from "../constants";

interface UploadFilesOptions { 
    password?: string;
    delete_at?: Date
    remaining_downloads?: number;
}

export type UploadIdentifier = string;
export const uploadFiles = async (files: File[], options: UploadFilesOptions): Promise<UploadIdentifier> => {
    if (files[0].name.length > MAX_FILE_NAME_SIZE) throw "Name of this file is too long, keep it below 80 characters"
    const beginUploadResponse = await post(UPLOAD_START_ENDPOINT, options);
    const uploadInfo = await beginUploadResponse.json()
    if (beginUploadResponse.status != 201) throw "Something went wrong!"
    const form = new FormData();
    form.set('file', files[0]);
    const uploadResponse = await post(`${UPLOAD_FILE_ENDPOINT}?id=${uploadInfo.identifier}`, form, ContentType.File)
    if (uploadResponse.status != 201) {
        // FIXME: Responsibility?
        await invalidateUpload(uploadInfo.identifier)
        throw "Your upload has been rejected. Either there is something wrong on our side or yours."
    }
    return uploadInfo.identifier
}

export const invalidateUpload = (uploadId: string) => {
    return get(`${INVALIDATE_UPLOAD_ENDPOINT}?id=${uploadId}`)
}