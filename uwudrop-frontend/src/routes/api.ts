interface UploadFilesOptions { 
    password?: string;
    expireAfter?: Date
}
export const uploadFiles = (files: File[], options: UploadFilesOptions) => {
    console.log(files)
    return new Promise(resolve => setTimeout(resolve, 5000))
}