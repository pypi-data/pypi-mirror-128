<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div class="modal" tabindex="-1" ref="replaceDialog">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body" ref="replaceDialogText"></div>
          <div class="modal-footer d-flex justify-content-between">
            <div class="form-check form-check-inline">
              <input type="checkbox" class="form-check-input" :id="`apply-all-${suffix}`" v-model="replaceApplyAll">
              <label class="form-check-label" :for="`apply-all-${suffix}`">{{ i18n.t('uploads.applyAll') }}</label>
            </div>
            <div>
              <button type="button"
                      class="btn btn-sm btn-light btn-modal"
                      data-dismiss="modal"
                      ref="replaceDialogBtnNo">
                {{ i18n.t('misc.no') }}
              </button>
              <button type="button"
                      class="btn btn-sm btn-primary btn-modal"
                      data-dismiss="modal"
                      ref="replaceDialogBtnYes">
                {{ i18n.t('misc.yes') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row align-items-end mb-2">
      <div class="col-lg-9 mb-2 mb-lg-0">
        <slot></slot>
      </div>
      <div class="col-lg-3 d-flex justify-content-end mb-2 mb-lg-0">
        <div class="w-100" v-if="experimentalFeatures">
          <dynamic-selection placeholder="Select a storage type."
                             container-classes="select2-single-sm"
                             :endpoint="getStorageTypesEndpoint"
                             :initial-values="[['local', 'local']]"
                             @select="selectStorage"
                             @unselect="unselectStorage">
          </dynamic-selection>
        </div>
      </div>
    </div>
    <upload-dropzone @add-file="addFile"></upload-dropzone>
    <input class="input" type="file" @change="inputChange" ref="input">
    <div class="card bg-light py-2 px-4 mt-4 mb-3" v-if="uploads.length > 0">
      <div class="form-row align-items-center">
        <div class="col-xl-8">
          {{ `${completedUploadsCount}/${uploads.length} ${i18n.t('uploads.completed', {count: uploads.length})}` }}
          <i class="fas fa-xs fa-check ml-2" v-if="completedUploadsCount === uploads.length"></i>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <small class="text-muted">{{ totalUploadSize | filesize }}</small>
        </div>
        <div class="col-xl-2 d-xl-flex justify-content-end">
          <div class="btn-group btn-group-sm">
            <button type="button"
                    class="btn btn-primary"
                    :title="i18n.t('uploads.resumeAll')"
                    :disabled="!resumable"
                    @click="resumeUploads(null)">
              <i class="fas fa-play"></i>
            </button>
            <button type="button"
                    class="btn btn-primary"
                    :title="i18n.t('uploads.pauseAll')"
                    :disabled="!pausable"
                    @click="pauseUploads(false)">
              <i class="fas fa-pause"></i>
            </button>
            <button type="button"
                    class="btn btn-primary"
                    :title="i18n.t('uploads.cancelAll')"
                    :disabled="!cancelable"
                    @click="cancelUploads(false)">
              <i class="fas fa-ban"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card"
         :class="{'mb-3': index < uploads.length - 1}"
         v-for="(upload, index) in paginatedUploads"
         :key="upload.id">
      <div class="card-body py-2">
        <div class="form-row align-items-center" :class="{'mb-2': upload.state !== 'completed'}">
          <div class="col-xl-8">
            <strong v-if="upload.state === 'completed'">
              <a :href="upload.viewFileEndpoint" v-if="upload.viewFileEndpoint">{{ upload.name }}</a>
              <span v-else>{{ upload.name }}</span>
            </strong>
            <span class="text-muted" v-else>{{ upload.name }}</span>
          </div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <small class="text-muted">{{ upload.size | filesize }}</small>
          </div>
          <div class="col-xl-2 d-xl-flex justify-content-end">
            <span class="badge badge-primary">{{ stateNames[upload.state] }}</span>
          </div>
        </div>
        <div class="form-row align-items-center" v-if="upload.state !== 'completed'">
          <div class="col-xl-10 py-1">
            <div class="progress border border-muted" style="height: 17px;">
              <div class="progress-bar" :style="{width: Math.floor(upload.progress) + '%'}">
                {{ Math.floor(upload.progress) }}%
              </div>
            </div>
          </div>
          <div class="col-xl-2 mt-2 mt-xl-0 d-xl-flex justify-content-end">
            <i class="fas fa-circle-notch fa-spin" v-if="upload.state === 'processing'"></i>
            <div class="btn-group btn-group-sm">
              <button type="button"
                      class="btn btn-light"
                      :title="i18n.t('uploads.pause')"
                      @click="pauseUploads(false, upload)"
                      v-if="isPausable(upload)">
                <i class="fas fa-pause"></i>
              </button>
              <button type="button"
                      class="btn btn-light"
                      :title="i18n.t('uploads.resume')"
                      @click="resumeUploads(upload)"
                      v-if="upload.state === 'paused'">
                <i class="fas fa-play" v-if="isResumable(upload)"></i>
                <i class="fas fa-folder-open" v-else></i>
              </button>
              <button type="button"
                      class="btn btn-light"
                      :title="i18n.t('uploads.cancel')"
                      @click="cancelUploads(false, upload)"
                      v-if="['pending', 'paused', 'uploading'].includes(upload.state)">
                <i class="fas fa-ban"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer bg-white py-1" v-if="upload.replacedFile !== null || upload.createdAt !== null">
        <div class="d-flex justify-content-between">
          <div>
            <div v-if="upload.replacedFile !== null">
              <span class="text-muted">{{ i18n.t('uploads.replaces') }}</span>
              <a class="text-muted" :href="upload.replacedFile._links.view">
                <strong>{{ upload.replacedFile.name }}</strong>
              </a>
            </div>
          </div>
          <div>
            <small class="text-muted" v-if="upload.createdAt !== null">
              {{ i18n.t('misc.createdAt') }} <local-timestamp :timestamp="upload.createdAt"></local-timestamp>
            </small>
          </div>
        </div>
      </div>
    </div>
    <pagination-control :total="uploads.length" :per-page="perPage" @update-page="page = $event"></pagination-control>
  </div>
</template>

<style scoped>
.btn-modal {
  width: 100px;
}

.input {
  position: absolute;
  visibility: hidden;
}
</style>

<script>
import UploadDropzone from 'scripts/lib/components/UploadDropzone.vue';
import ChunkedUploadStorage from 'scripts/lib/storage/chunked.js';
import DirectUploadStorage from 'scripts/lib/storage/direct.js';

export default {
  components: {
    UploadDropzone,
  },
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      storages: {},
      selectedStorage: {
        storageType: 'local',
        uploadType: 'chunked',
      },
      uploads: [],
      uploadQueue: [],
      addedFileTimeoutHandle: null,
      resumedUpload: null,
      replaceApplyAll: false,
      page: 1,
      stateNames: {
        paused: i18n.t('uploads.statePaused'),
        pending: i18n.t('uploads.statePending'),
        uploading: i18n.t('uploads.stateUploading'),
        processing: i18n.t('uploads.stateProcessing'),
        completed: i18n.t('uploads.stateCompleted'),
      },
    };
  },
  props: {
    newUploadEndpoint: String,
    getUploadsEndpoint: String,
    getStorageTypesEndpoint: String,
    directUploadEndpoint: String,
    experimentalFeatures: {
      type: Boolean,
      default: kadi.globals.experimental_features,
    },
    perPage: {
      type: Number,
      default: 5,
    },
  },
  computed: {
    paginatedUploads() {
      return kadi.utils.paginateList(this.uploads, this.page, this.perPage);
    },
    totalUploadSize() {
      /* eslint-disable no-param-reassign */
      return this.uploads.reduce((acc, upload) => acc += upload.size, 0);
    },
    completedUploadsCount() {
      return this.uploads.reduce((acc, upload) => (upload.state === 'completed' ? acc += 1 : acc), 0);
      /* eslint-enable no-param-reassign */
    },
    uploadInProgress() {
      return this.uploads.slice().some((upload) => upload.state === 'uploading');
    },
    pausable() {
      return this.uploads.slice().some((upload) => this.storages[upload.uploadType].isPausable(upload));
    },
    resumable() {
      return this.uploads.slice().some((upload) => this.isResumable(upload));
    },
    cancelable() {
      return this.uploads.slice().some((upload) => ['pending', 'uploading', 'paused'].includes(upload.state));
    },
  },
  watch: {
    uploadQueue() {
      // When adding lots of files simultaneously, wait until they have all been added to the queue before uploading.
      if (this.addedFileTimeoutHandle !== null) {
        window.clearTimeout(this.addedFileTimeoutHandle);
      }

      this.addedFileTimeoutHandle = window.setTimeout(() => this.uploadNextFile(), 100);
    },
  },
  methods: {
    addFile(file, force = false, origin = null) {
      const upload = this.storages[this.selectedStorage.uploadType].open({
        file,
        name: file.name,
        size: file.size,
        forceReplace: force,
        origin,
        storageType: this.selectedStorage.storageType,
      });

      this.uploadQueue.push(upload);
      this.uploads.push(upload);
    },

    confirmReplace(upload) {
      return new Promise((resolve) => {
        $(this.$refs.replaceDialog).modal({backdrop: 'static', keyboard: false});
        this.$refs.replaceDialogText.innerText = i18n.t('warning.replaceUpload', {filename: upload.name});

        let cancelUploadHandler = null;
        let replaceFileHandler = null;

        // Make sure that the event listeners are removed again and the checkbox is reset after resolving the promise by
        // closing the modal via one of the buttons.
        const resolveDialog = (status) => {
          resolve({status, applyAll: this.replaceApplyAll});
          this.replaceApplyAll = false;
          this.$refs.replaceDialogBtnNo.removeEventListener('click', cancelUploadHandler);
          this.$refs.replaceDialogBtnYes.removeEventListener('click', replaceFileHandler);
        };

        cancelUploadHandler = () => resolveDialog(false);
        replaceFileHandler = () => resolveDialog(true);

        this.$refs.replaceDialogBtnNo.addEventListener('click', cancelUploadHandler);
        this.$refs.replaceDialogBtnYes.addEventListener('click', replaceFileHandler);
      });
    },

    selectStorage(selection) {
      this.selectedStorage.storageType = selection.id;
      this.selectedStorage.uploadType = selection.upload_type;
    },

    unselectStorage() {
      this.selectedStorage.storageType = 'local';
      this.selectedStorage.uploadType = 'chunked';
    },

    inputChange(e) {
      const file = e.target.files[0];
      if (file.size !== this.resumedUpload.size) {
        if (!window.confirm(i18n.t('warning.uploadSizeDiffers'))) {
          return;
        }
      }

      if (file.name !== this.resumedUpload.name) {
        if (!window.confirm(i18n.t('warning.fileNameDiffers'))) {
          return;
        }
      }

      this.resumedUpload.file = file;
      this.resumedUpload.state = 'pending';
      this.uploadQueue.push(this.resumedUpload);
    },

    async handleFileReplacement(upload) {
      if (upload.forceReplace) {
        return true;
      }

      // Show a confirmation dialog.
      const input = await this.confirmReplace(upload);

      // Either mark all files to be replaced or just continue with the upload as normal.
      if (input.status && input.applyAll) {
        for (const _upload of this.uploads.slice()) {
          _upload.forceReplace = true;
        }
      // If applicable, mark all current uploads to be skipped and cancel the current upload.
      } else if (!input.status) {
        // Mark all pending uploads as not to be replaced.
        if (input.applyAll) {
          for (const _upload of this.uploads.slice()) {
            _upload.skipReplace = true;
          }
        }

        // Cancel the current upload either way.
        this.cancelUploads(true, upload);
        return false;
      }

      return true;
    },

    async handleFileExists(upload) {
      // Existing file should not be replaced.
      if (upload.skipReplace) {
        this.cancelUploads(true, upload);
        return false;
      }

      // Ask the user if the file should be replaced.
      const replacedByUser = await this.handleFileReplacement(upload);
      return replacedByUser;
    },

    async handleError(error, upload) {
      if (error.request.status === 409) {
        // Handle file already existing.
        const replaceFile = await this.handleFileExists(upload);
        return replaceFile;
      }

      // Some quota was exceeded.
      if (error.request.status === 413) {
        // Use the error message from the backend.
        kadi.alert(error.response.data.description, {type: 'warning'});
      } else {
        kadi.alert(i18n.t('error.initiateUpload'), {request: error.request});
      }

      this.cancelUploads(true, upload);
      return false;
    },

    async uploadNextFile() {
      // Check precondition to start the next upload. There will be only one upload at a time.
      if (this.uploadQueue.length === 0 || this.uploadInProgress) {
        return;
      }

      // Get the next upload in the queue.
      const upload = this.uploadQueue[0];

      // Check if the upload was already started just in case.
      if (upload.state !== 'pending') {
        return;
      }

      upload.state = 'uploading';

      // Start the actual upload of the file.
      await this.storages[upload.uploadType].save(upload);

      // Remove the upload from the queue regardless of whether it was successful or not. At this point, the storage
      // tried its best to upload the file, so we are done.
      kadi.utils.removeFromList(this.uploadQueue, upload);
    },

    cancelUploads(force, upload = null) {
      const _removeUpload = (upload) => {
        kadi.utils.removeFromList(this.uploadQueue, upload);
        kadi.utils.removeFromList(this.uploads, upload);
        this.$emit('upload-canceled', upload, upload.origin);
      };

      let uploads = [];
      let message = '';

      if (upload === null) {
        uploads = this.uploads.slice();
        message = i18n.t('warning.cancelUploads');
      } else {
        uploads.push(upload);
        message = i18n.t('warning.cancelUpload', {filename: upload.name});
      }

      if (!force && !window.confirm(message)) {
        return;
      }

      for (const _upload of uploads) {
        // If the upload is already processing or completed we just ignore the cancel request.
        if (!force && ['processing', 'completed'].includes(_upload.state)) {
          continue;
        }

        // Cancel the current request if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        // Cancel the storage specific upload.
        this.storages[_upload.uploadType].cancel(_upload)
          .then(() => _removeUpload(_upload))
          .catch((error) => {
            if (error.request.status !== 404) {
              kadi.alert(i18n.t('error.removeUpload'), {request: error.request});
            } else {
              _removeUpload(_upload);
            }
          });
      }
    },

    pauseUploads(force, upload = null) {
      let uploads = [];
      if (upload === null) {
        uploads = this.uploads.slice();
      } else {
        uploads.push(upload);
      }

      for (const _upload of uploads) {
        const storage = this.storages[_upload.uploadType];

        if (!storage.isPausable(_upload)) {
          continue;
        }

        _upload.state = 'paused';

        // Cancel the current request if possible.
        if (_upload.source) {
          _upload.source.cancel();
          _upload.source = null;
        }

        kadi.utils.removeFromList(this.uploadQueue, _upload);
      }
    },

    resumeUploads(upload = null) {
      if (upload !== null) {
        if (this.isResumable(upload)) {
          // The upload was started in the current session or has no missing chunks.
          upload.state = 'pending';
          this.uploadQueue.push(upload);
        } else {
          // The upload was started in a previous session and is still missing chunks.
          this.resumedUpload = upload;
          this.$refs.input.click();
        }
      } else {
        // We only take the first case mentioned above into account for bulk resuming.
        for (const _upload of this.uploads.slice()) {
          if (this.isResumable(_upload)) {
            _upload.state = 'pending';
            this.uploadQueue.push(_upload);
          }
        }
      }
    },

    isResumable(upload) {
      return this.storages[upload.uploadType].isResumable(upload);
    },

    isPausable(upload) {
      return ['pending', 'uploading'].includes(upload.state) && upload.uploadType === 'chunked';
    },

    beforeUnload(e) {
      if (this.uploadQueue.length > 0) {
        e.preventDefault();
        (e || window.event).returnValue = '';
        return '';
      }
      return null;
    },
  },
  mounted() {
    const chunkedUploadStorage = new ChunkedUploadStorage(this.newUploadEndpoint, this.getUploadsEndpoint);

    chunkedUploadStorage.onComplete((upload, data) => this.$emit('upload-completed', data._meta.file, upload.origin));
    chunkedUploadStorage.onPause(this.pauseUploads);
    chunkedUploadStorage.onCancel(this.cancelUploads);
    chunkedUploadStorage.onError(this.handleError);

    this.storages.chunked = chunkedUploadStorage;

    const directUploadStorage = new DirectUploadStorage(this.directUploadEndpoint);

    directUploadStorage.onComplete((upload, data) => this.$emit('upload-completed', data, upload.origin));
    directUploadStorage.onPause(this.pauseUploads);
    directUploadStorage.onCancel(this.cancelUploads);
    directUploadStorage.onError(this.handleError);

    this.storages.direct = directUploadStorage;

    // Get the active uploads so the user can resume them.
    chunkedUploadStorage.loadUploads()
      .then((fetchedUploads) => {
        this.uploads = this.uploads.concat(fetchedUploads);
      })
      .catch((error) => {
        kadi.alert(i18n.t('error.loadUploads'), {request: error.request});
      });

    window.addEventListener('beforeunload', this.beforeUnload);

    // Move the modal replace dialog to the document body so it is always shown, even if the upload manager is not
    // visible, and to also avoid general rendering issues.
    document.getElementsByTagName('body')[0].appendChild(this.$refs.replaceDialog);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.beforeUnload);
    $(this.$refs.replaceDialog).modal('dispose');
  },
};
</script>
