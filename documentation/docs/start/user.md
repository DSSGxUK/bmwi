# User Worlflow

<!-- load mermaid -->
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:true});
mermaidAPI.initialize({
    securityLevel: 'loose'
});
</script>

<!-- **Pro Tip**: Clicking on the purple nodes leads to the specific step in the documentation. -->
<!-- **Pro Tip**: Clicking on the purple nodes leads to the tool page. -->

<div class="mermaid">
graph TD
    subgraph clean data
    A[Dataset Prep page: time-series excel workbook]
    end
    subgraph VAR model walkforward
    B[Predictions page: unemployment rate forecasting on Kreis-level]
    end
    subgraph interpret predictions
    D[Visualization page: line plot, map of Germany]
    E[Ranking page: kreise rankings and grouped rankings]
    D --> E
    end
    subgraph validate predictions
    F[Error Analysis page: compare structural, crisis-time data]
    end
    A --> B
<!-- <<<<<<< vighnesh_docs_work
    D -.-> E
    D -.-> F
    click A "../../steps/data_prep/"
    click B "../../steps/model/#fit-model-and-export-predictions"
    click C "../../steps/model/#visualize-prediction-results"
    click E "../../steps/error/"
    click F "../../steps/home/"
</div>
======= -->
    B --> D
    E --> F
</div>

</br>

<!-- <div>
    click A "http://127.0.0.1:8000/steps/data_prep/"
    click B "http://127.0.0.1:8000/steps/model/#fit-model-and-export-predictions"
    click C "http://127.0.0.1:8000/steps/model/#visualize-prediction-results"
    click D "https://github.com/prakharrathi25/the-tool-bmwi/blob/main/pages/model_v1.py"
    click E "http://127.0.0.1:8000/steps/error/"
    click F "http://127.0.0.1:8000/steps/home/"
</div> -->
<!-- >>>>>>> main -->
