<script lang="ts">
    import {FileDropzone, Headline, Subhead, FormField, TextField, TimePicker, DatePicker, Divider, Button, Loading, H3} from 'attractions'
    import { uploadFiles } from './api';
    import { DONWLOAD_ENDPOINT, WEB_URL} from '../constants'

    let files: File[] = []

    let password : string | undefined = undefined
    let maxDownloads : number | undefined = undefined
    const maxDate = (() => {
        const date = new Date()
        date.setDate(date.getDate() + 7)
        return date
    })()
    let expireAfter : Date = maxDate
    let requestStatus: Promise<string> | undefined = undefined
    const upload = () => {
        requestStatus = uploadFiles(files, { password, delete_at: expireAfter, remaining_downloads: maxDownloads })
            .then(s => `${WEB_URL}${DONWLOAD_ENDPOINT}${s}`)
    }

    $: if (expireAfter > maxDate) expireAfter = maxDate
    $: if (files.length > 0) requestStatus = undefined

</script>

<div class="w-full align-center p-10">
    <Headline>uwudrop - a quick file sharing site</Headline>
    <Subhead>Just drop a file and hit upload!</Subhead>
    <Subhead>Only one - if you need more, archive them on your own.</Subhead>
    <Subhead>I don't care about any file extensions.</Subhead>
    <Subhead>Any illegal files will be removed. Uploader then is going to get banned and reported to authorithies</Subhead>
    <Subhead>Files are kept for 7 days. </Subhead>
    <Subhead>Maximum file size is 500 MB.</Subhead>

    <FileDropzone name="file" max={1} bind:files></FileDropzone>
    <div class="upload-settings my-5">
        <FormField name="Password" help="This password will be required to download the file" optional>
            <TextField bind:value={password} type="password"/>
        </FormField>
        <FormField name="Downloads" help="File will be removed after specified number of downloads (max. 2000)" optional>
            <TextField bind:value={maxDownloads} type="number" max={2000}/>
        </FormField>
        <FormField name="Expire after:">
        <DatePicker bind:value={expireAfter}/> <TimePicker bind:value={expireAfter}/>
        </FormField>
        <Divider/>
        {#if !requestStatus}
            <Button filled class="my-5 mx-auto" on:click={upload}>Upload</Button>
        {/if}
        {#await requestStatus}
            <Loading class="text-3xl py-10"/>
        {:then url}
            {#if requestStatus}
                <div>
                    <H3>Your download link: <a href={url}>{url}</a></H3>
                </div>
            {/if}
        {:catch err}
            <H3 class="text-red-500 text-xl">{err}</H3>
            <Button filled class="my-5 mx-auto" on:click={upload}>Upload</Button>
        {/await}
    </div>
</div>
