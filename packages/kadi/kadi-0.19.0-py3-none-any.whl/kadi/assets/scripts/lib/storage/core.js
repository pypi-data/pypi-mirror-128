/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

export default class BaseStorage {
  constructor() {
    this.uploadType = null;
  }

  open(config) {
    return {
      storageType: config.storageType,
      uploadType: this.uploadType,
      id: kadi.utils.randomAlnum(), // For use in v-for before the upload has an actual ID.
      name: config.name,
      state: 'pending',
      origin: config.origin, // To distinguish where an upload originated from.
      forceReplace: config.forceReplace, // To force replacing an existing file without warning the user.
      skipReplace: false, // To skip replacing an existing file without warning the user.
      progress: 0,
      source: null,
      replacedFile: null,
      createdAt: null,
      viewFileEndpoint: null,
    };
  }

  save() {
    throw new Error(`Implement abstract method "save" to save files in storage '${this.uploadType}'.`);
  }

  cancel() {
    throw new Error(`Implement abstract method "cancel" to cancel uploads to storage '${this.uploadType}'.`);
  }

  getUploadProgress() {
    throw new Error('Implement abstract method "getUploadProgress" to get the progress of uploads for storage'
                     + ` '${this.storageType}'.`);
  }

  isPausable() {
    throw new Error(`Implement abstract method "isPausable" to check if an upload to storage '${this.uploadType}' can`
                    + ' be paused.');
  }

  isResumable() {
    throw new Error(`Implement abstract method "isResumable" to check if an upload to storage '${this.uploadType}' can`
                     + ' be resumed.');
  }

  onPause(pauseCallback) {
    this.pauseCallback = pauseCallback;
  }

  onCancel(cancelCallback) {
    this.cancelCallback = cancelCallback;
  }

  onComplete(uploadCompleteCallback) {
    this.uploadCompleteCallback = uploadCompleteCallback;
  }

  onError(errorCallback) {
    this.errorCallback = errorCallback;
  }
}
