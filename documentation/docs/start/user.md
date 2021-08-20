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
    end
    subgraph validate predictions
        F[Error Analysis page: compare structural, crisis-time data]
    end
    A --> B
    D --> E

    B --> D
    E --> F

    click A "../../steps/data_prep/"
    click B "../../steps/model/#fit-model-and-export-predictions"
    click D "../../steps/visualizations/"
    click E "../../steps/rankings/"
    click F "../../steps/error/"
</div>

</br>
