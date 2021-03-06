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
        A[Dataset Preparation: time-series excel workbook]
    end
    subgraph VAR model walkforward
        B[Predictions: unemployment rate forecasting on Kreis-level]
        C[Confidence Intervals: defaulted 95% confidence for predictions]
    end
    subgraph interpret predictions
        D[Visualizations: line plot, map of Germany and Bundesland]
        E[Rankings: kreise rankings and grouped rankings with line plots]
    end
    subgraph validate predictions
        F[Error Analysis: compare and get important structural data]
    end
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F

    click A "../../steps/data_prep/"
    click B "../../steps/model/#fit-model-and-export-predictions"
    click D "../../steps/visualizations/"
    click E "../../steps/rankings/"
    click F "../../steps/error/"
</div>

</br>
