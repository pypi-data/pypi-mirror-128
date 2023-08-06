<!-- Copyright 2021 Karlsruhe Institute of Technology
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
    <div class="row mb-2">
      <div class="col-sm-4 mb-2 mb-sm-0">
        <a class="btn btn-sm btn-light" :href="downloadEndpoint">
          <i class="fas fa-download"></i>
          Download
        </a>
      </div>
      <div class="col-sm-8 d-sm-flex justify-content-end" v-if="isCustomizable">
        <button class="btn btn-sm btn-light mr-2" :disabled="loading" @click="updatePreview" v-if="showUpdateButton">
          <i class="fas fa-eye"></i>
          Update preview
        </button>
        <collapse-item :id="`collapse-${suffix}`"
                       :is-collapsed="true"
                       class="btn btn-sm btn-light"
                       @collapse="showUpdateButton = !$event">
          Customize
        </collapse-item>
      </div>
    </div>
    <div class="card mb-4 collapse" :id="`collapse-${suffix}`" v-if="isCustomizable">
      <div class="card-body">
        <strong>Export data to exclude</strong>
        <hr class="mt-0">
        <div class="form-check form-check-inline mb-2">
          <input type="checkbox" class="form-check-input" :id="`user-${suffix}`" v-model="filter.user">
          <label class="form-check-label" :for="`user-${suffix}`">User information</label>
        </div>
        <div v-if="resourceType === 'record'">
          <div class="form-check form-check-inline mb-2">
            <input type="checkbox" class="form-check-input" :id="`collections-${suffix}`" v-model="filter.collections">
            <label class="form-check-label" :for="`collections-${suffix}`">Collections</label>
          </div>
          <br>
          <label class="form-control-label" :for="`links-${suffix}`">Record links</label>
          <select class="custom-select custom-select-sm" :id="`links-${suffix}`" v-model="filter.links">
            <option value=""></option>
            <option value="out">Outgoing</option>
            <option value="in">Incoming</option>
            <option value="both">Both</option>
          </select>
          <div v-if="extras.length > 0">
            <div class="my-2">Extra metadata</div>
            <div class="card bg-light">
              <div class="card-body">
                <extras-selector :extras="extras" :use-indices="true" @select="filter.extras = $event">
                </extras-selector>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!loading" ref="preview">
      <div v-if="exportType === 'json'">
        <div class="card bg-light">
          <div class="mt-3 ml-3">
            <pre class="text">{{ exportData }}</pre>
          </div>
        </div>
      </div>
      <div v-if="exportType === 'pdf'">
        <iframe class="w-100 vh-75 border border-muted rounded" frameborder="0" allowfullscreen :src="exportData">
        </iframe>
      </div>
      <div v-if="exportType === 'qr'">
        <div class="border border-muted bg-light text-center">
          <img class="img-fluid" :src="exportData">
        </div>
      </div>
    </div>
    <i class="fas fa-circle-notch fa-spin mt-3" v-else></i>
  </div>
</template>

<style scoped>
.text {
  max-height: 75vh;
}
</style>

<script>
export default {
  data() {
    return {
      suffix: kadi.utils.randomAlnum(), // To create unique IDs.
      exportData: null,
      loading: true,
      showUpdateButton: false,
      filter: {
        user: false,
        collections: false,
        links: '',
        extras: {},
      },
    };
  },
  props: {
    resourceType: String,
    exportType: String,
    endpoint: String,
    extras: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    downloadEndpoint() {
      return `${this.endpoint}?download=true&filter=${this.getFilterString()}`;
    },
    isCustomizable() {
      return ['json', 'pdf'].includes(this.exportType);
    },
  },
  methods: {
    getFilterString() {
      const filter = {};

      if (this.filter.user !== false) {
        filter.user = this.filter.user;
      }
      if (this.filter.collections !== false) {
        filter.collections = this.filter.collections;
      }
      if (this.filter.links !== '') {
        filter.links = this.filter.links;

        if (filter.links === 'both') {
          filter.links = true;
        }
      }
      if (Object.keys(this.filter.extras).length > 0) {
        filter.extras = this.filter.extras;
      }

      return JSON.stringify(filter);
    },
    updateExportData(scrollIntoView = false) {
      this.loading = true;

      axios.get(this.endpoint, {params: {filter: this.getFilterString()}})
        .then((response) => {
          this.exportData = response.data;
          this.loading = false;

          if (scrollIntoView) {
            this.$nextTick(() => kadi.utils.scrollIntoView(this.$refs.preview, 'top'));
          }
        })
        .catch((error) => kadi.alert(i18n.t('error.loadExportData'), {request: error.request}));
    },
    updatePreview() {
      this.updateExportData(true);
    },
  },
  mounted() {
    this.updateExportData();
  },
};
</script>
