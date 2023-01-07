<script lang="ts">
    import {FileDropzone, Headline, Subhead, FormField, TextField, TimePicker, DatePicker, Divider, Button, Loading} from 'attractions'
    import { uploadFiles } from './api';

    let files: File[] = []

    let password : string | undefined = undefined
    let downloads : number | undefined = undefined
    const maxDate = (() => {
        const date = new Date()
        date.setDate(date.getDate() + 7)
        return date
    })()
    let expireAfter : Date = maxDate
    let requestStatus: Promise<any> | undefined = undefined
    const upload = () => {
        requestStatus = uploadFiles(files, { password, expireAfter }).then(() => requestStatus = undefined)
    }

    $: if (expireAfter > maxDate) expireAfter = maxDate

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
            <TextField bind:value={password}/>
        </FormField>
        <FormField name="Downloads" help="File will be removed after specified number of downloads" optional>
            <TextField bind:value={downloads} type="number"/>
        </FormField>
        <FormField name="Expire after:">
        <DatePicker bind:value={expireAfter}/> <TimePicker bind:value={expireAfter}/>
        </FormField>
        <Divider/>
            {#if !requestStatus}
                <Button filled class="my-5 mx-auto" on:click={upload}>Upload</Button>
            {:else}
                {#await requestStatus}
                    <Loading class="text-3xl py-10"/>
                {/await}
            {/if}
    </div>
</div>
