# Technical Workflow

<!-- load mermaid -->
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:true});
mermaidAPI.initialize({
    securityLevel: 'loose'
});
</script>

**Pro Tip**: Clicking on the purple nodes leads to the source code.

<!-- **Pro Tip**: Clicking on the purple nodes leads to the tool page. -->

<div class="mermaid">
graph TD
    subgraph Dataset Prep page
    A[time-series excel workbook with CleanerClass]
    end
    subgraph Model page
    B[Unemployment Rate Prediction on Kreis-level]
    C[Visualization: line plot, map of Germany]
    D[Output file: single excel worksheet]
    B --> C --> D
    end
    subgraph Error Analysis page
    E[Error Analysis]
    end
    subgraph Home page
    F[rankings & groups]
    end
    A --> B
    D --> E
    D --> F
    click A "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/data_prep.py"
    click B "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/model_page.py"
    click C "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/prediction_viz.py"
    click D "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/model_page.py"
    click E "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/error_analysis.py"
    click F "https://github.com/prakharrathi25/the-tool-bmwi/blob/814aeeac9fff59c19286c86534a11476cf801f52/pages/ranking.py"
</div>